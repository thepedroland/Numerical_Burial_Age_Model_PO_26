% all calculations using the basin shapes in : /Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/PhD_Amazon_Project_1st_chapter/results_lab/erosion_rates_calculation/basin_dir

addpath(genpath('/Users/pedro_oliveira/Documents/topotoolbox-master'));
addpath(genpath('/Users/pedro_oliveira/Documents/Topographic-Analysis-Kit-master'));

%%
DEM = GRIDobj('/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/1_PhD_PAPER_1/data/support/DEM_full_30m.tif');
DEM = reproject2utm(DEM,30);
[DEM,FD,A,S]=MakeStreams(DEM,1e7,"no_data_exp",'DEM<5');


imageschs(DEM)
hold on
plot(S,"-r")


%%

river_mouths = [];
for i=1:16
    load(sprintf("Basin_%d_Data",i))
    river_mouths(i,:) = RiverMouth;
end
BasinPicker

%%

ProcessRiverBasins(DEM,FD,A,S,[347525 9694890,8],'basin_dir')

%% 
relief_basins = {}
for i = 1:16
    load(sprintf("Basin_%d_Data",i))
    for j =1:4
    relief_basins{i,j} = rlf_stats(j,1)
    end
end
%%
imageschs(DEMoc)
%%

%%
relief_basins = cell(16,5);
relief_basins_std = cell(16,5);

reliefs = [1000,1500,2000,2500,3000];

for i=1:16
    load(sprintf("Basin_%d_Data",i));
    for j =1:5
        H = localtopography(DEMoc,reliefs(j));
        avr_H = mean(H.Z,"all","omitmissing");
        std_H = std(H.Z,[],"all","omitmissing");
        relief_basins{i,j} = avr_H;
        relief_basins_std{i,j} = std_H;

    end
end
writecell(relief_basins,'/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/py_repositories/numerical_MC_Burial_Ages_PO/support/data/relief_basins_data.csv')
writecell(relief_basins_std,'/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CUNY/PhD_LIFE/py_repositories/numerical_MC_Burial_Ages_PO/support/data/relief_basins_data_std.csv')
