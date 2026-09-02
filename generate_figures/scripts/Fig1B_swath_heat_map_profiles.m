%POINT DENSITY SWATH PROFILE
%pedro_oliveira
%AUG,19,2026

addpath(genpath('/Users/pedro_oliveira/Documents/topotoolbox-master'));
addpath(genpath('/Users/pedro_oliveira/Documents/Topographic-Analysis-Kit-master'));
addpath('/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/py_repositories/numerical_MC_Burial_Ages_PO/support/aux_functions/mat_codes/modified_functions')
addpath('/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/1_PhD_PAPER_1/data/data_swath')

clear all;
save_path_img = "/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/1_PhD_PAPER_1/illustrations";

%%% --- SETUP UP PLOT --- %%%
sample = string("bv");
recrop_DEM = false;
re_extract_swath = false; 
sample_file_name = sprintf('%s_terrace_info',sample)
save_file_loc = '/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/1_PhD_PAPER_1/data/data_swath'
user_colormap = "oslo";
%%% ----------------
if recrop_DEM == true

    DEM = GRIDobj('/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/PhD_Amazon_Project_1st_chapter/results_lab_(1)/GIS/DEM_full_area.tif');
    DEM = reproject2utm(DEM,30);
    
    %%CROP DEM IF NEEDED
    
    MASK = createmask(DEM);
    terrace_DEM = crop(DEM,MASK,NaN);
    imagesc(terrace_DEM)

    save(terrace_DEM,"DEM_terraces");
end

if re_extract_swath == true

    load('DEM_terraces');

    % Run swath extraction once (no immediate saving)
    [SW,SwathMat,xypoints,bends] = MakeTopoSwath_MOD_Oliveira(terrace_DEM,[],5000,'plot_as_heatmap',true,'save_figure',true,"vex",100,'make_shape',true,"location_id",sample,"user_colormap",user_colormap);
    % [SW,SwathMat,xypoints,bends] = MakeTopoSwath(terrace_DEM,[],5000);

    % Ask user whether to save the profile or redo it
    choice = questdlg('Do you want to save this profile or redo it?', ...
        'Save or Redo', ...
        'Save','Redo','Cancel','Save');

    switch choice
        case 'Save'
            % Save variables to a MAT file named with the sample id
            mat_fname = fullfile(save_file_loc, sprintf('%s_terrace_info.mat', sample));
            save(mat_fname, 'SW', 'SwathMat', 'xypoints', 'bends');

            % Informative message
            fprintf('Saving density point swath profile for sample: %s\n', sample);

            % Save figure using save_path_img with dynamic filename
            filename = fullfile(save_path_img, sprintf('Swath-profile_sample_%s_density_point.png', sample));
            print(gcf, filename, '-dpng', '-r700');

            fig_name = sprintf('Swath-profile_sample_%s_density_point', sample);
            readme_path = fullfile(save_path_img, sprintf('/README_FILES/README_fig_%s.txt', fig_name));

            % 2. Get metadata
            script_path = which(mfilename);
            if isempty(script_path)
                script_path = matlab.desktop.editor.getActiveFilename; % fallback when running in live/script editor
            end
            current_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');

            % 3. Write the file
            fileID = fopen(readme_path, 'w');
            if fileID == -1
                error('Cannot open file for writing: %s', readme_path);
            end

            fprintf(fileID, '# %s heat map\n\n', fig_name);
            fprintf(fileID, 'The figure was generated using code: %s\n', script_path);
            fprintf(fileID, 'Date: %s\n', current_time);
            fprintf(fileID, 'Sample ID: %s\n', sample);

            fclose(fileID);

            % Print success message to console
            fprintf('Metadata saved successfully to: %s\n', readme_path);

            close all;

        case 'Redo'
            % Close current figure and rerun MakeTopoSwath allowing user to interact again.
            close all;
            % Re-run swath extraction and show plot again without saving.
            [SW,SwathMat,xypoints,bends] = MakeTopoSwath_MOD_Oliveira(terrace_DEM,[],5000,'plot_as_heatmap',true,'save_figure',false,"vex",50,"user_colormap",user_colormap);

            % After redoing, ask again (recursive-like loop)
            redo_choice = questdlg('Do you want to save this new profile or redo again?', ...
                'Save or Redo', ...
                'Save','Redo','Cancel','Save');
            if strcmp(redo_choice,'Save')
                mat_fname = sprintf('%s_terrace_info.mat', sample);
                save(mat_fname, 'SW', 'SwathMat', 'xypoints', 'bends');
                filename = fullfile(save_path_img, sprintf('Swath-profile_sample_%s_density_point.png', sample));
                print(gcf, filename, '-dpng', '-r700');
                fig_name = sprintf('Swath-profile_sample_%s_density_point', sample);
                readme_path = fullfile(save_path_img, sprintf('/README_FILES/README_fig_%s.txt', fig_name));
                script_path = which(mfilename);
                if isempty(script_path)
                    script_path = matlab.desktop.editor.getActiveFilename;
                end
                current_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');
                fileID = fopen(readme_path, 'w');
                if fileID == -1, error('Cannot open file for writing: %s', readme_path); end
                fprintf(fileID, '# %s heat map\n\n', fig_name);
                fprintf(fileID, 'The figure was generated using code: %s\n', script_path);
                fprintf(fileID, 'Date: %s\n', current_time);
                fprintf(fileID, 'Sample ID: %s\n', sample);
                fclose(fileID);
                fprintf('Metadata saved successfully to: %s\n', readme_path);
                close all;
            elseif strcmp(redo_choice,'Redo')
                % If user chooses to redo again, re-enter this block by setting re_extract_swath true
                % and returning control to outer logic (simple approach: throw a flag and re-run script manually)
                warning('User requested multiple redos. Re-run the script section to generate another profile.');
                close all;
            else
                % Cancel selected after redo: do nothing
                close all;
            end

        otherwise % 'Cancel' or closed dialog
            fprintf('User cancelled saving. No files were written.\n');
            close all;
    end

else

    load(sample_file_name);

    points_profile(1,1) = xypoints(1,1);
    points_profile(1,2) = xypoints(1,2);
    points_profile(2,1) = xypoints(length(xypoints),1);
    points_profile(2,2) = xypoints(length(xypoints),2);

    load("DEM_terraces.mat");
    [SW,SwathMat,xypoints,bends] = MakeTopoSwath_MOD_Oliveira(terrace_DEM,points_profile,10000,'plot_as_heatmap',true,'save_figure',true,"vex",50,"user_colormap",user_colormap,'make_shape',true,"location_id",sample);
    % mat_fname = sprintf('%s_terrace_info.mat', sample);
    % save(mat_fname, 'SW', 'SwathMat', 'xypoints', 'bends');
    % filename = fullfile(save_path_img, sprintf('Swath-profile_sample_%s_density_point.png', sample));
    % exportgraphics(gcf, filename,'Resolution', 700);
    % axis on 
    % filename = fullfile(save_path_img, sprintf('Swath-profile_sample_%s_density_point.svg', sample));
    % exportgraphics(gcf, filename, 'ContentType', 'vector');

    
end