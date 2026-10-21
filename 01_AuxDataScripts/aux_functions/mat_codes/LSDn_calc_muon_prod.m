function [p_neg_list, p_fast_list, Rc_list] = calc_muon_prod_LSDn_Balco(time_list, depth_list, nuclide, Rc_value)
% calc_muon_prod_LSDn_Balco - vectorized version
%
% Accepts equal-length vectors time_list and depth_list, paired by index
% (i.e. depth_list(i) corresponds to time_list(i)), and returns one
% p_neg / p_fast / Rc value per input pair.
%
% nuclide   : 'be' or 'al'
% Rc_value  : 'max', 'min', 'mean', or anything else -> per-time lookup
%             against the Rc_results.csv table (same logic as original).
%
% Internally, P_mu_totalLSD accepts a *vector* of depths but only a
% single Rc value per call. Since Rc can differ across rows (it depends
% on time), rows are grouped by identical Rc and P_mu_totalLSD is called
% once per unique Rc group, rather than once per row.

    time_list = time_list(:);
    depth_list = depth_list(:);

    if numel(time_list) ~= numel(depth_list)
        error('time_list and depth_list must be the same length');
    end
    n = numel(time_list);

    main_path = fileparts(fileparts(fileparts(mfilename('fullpath'))));
    addpath(fullfile(main_path,"aux_functions","mat_codes","balco_2018_muogenic_prod"));
    load(fullfile(main_path,"aux_functions", "mat_codes","balco_2018_muogenic_prod", "consts_LSD.mat"));

    Rc_table = readmatrix(fullfile(main_path,"data/TopographicData","Rc_results.csv"));
    times_table = Rc_table(1,:).*50000;

    % ---- determine Rc for every (time, depth) pair ----
    Rc_list = nan(n,1);

    if strcmpi(Rc_value, "max")
        Rc_list(:) = max(Rc_table(2,:));
    elseif strcmpi(Rc_value, "min")
        Rc_list(:) = min(Rc_table(2,:));
    elseif strcmpi(Rc_value, "mean")
        Rc_list(:) = mean(Rc_table(2,:));
    else
        Rc_list = arrayfun(@(t) lookup_Rc(t, times_table, Rc_table), time_list);
    end

    % ---- constants shared across all calls ----
    elevation = 11;
    atm_depth = ERA40atm(-2,-58,elevation);
    SPhi = consts.SPhiInf;

    switch lower(nuclide)
        case 'be'
            mc.Natoms   = 2.006e22;
            mc.k_neg    = consts.k_neg10;
            mc.sigma0   = consts.sigma190_10./190;
            mc.mfluxRef = consts.mfluxRef;
        case 'al'
            mc.Natoms   = 1.003e22;
            mc.k_neg    = consts.k_neg26;
            mc.sigma0   = consts.sigma190_26./190;
            mc.mfluxRef = consts.mfluxRef;
        otherwise
            error('nuclide must be ''be'' or ''al''');
    end

    % ---- group by unique Rc so P_mu_totalLSD is called once per group ----
    p_neg_list  = nan(n,1);
    p_fast_list = nan(n,1);

    [unique_Rc, ~, group_idx] = unique(Rc_list);

    for g = 1:numel(unique_Rc)
        this_Rc = unique_Rc(g);
        mask = (group_idx == g);
        z_group = depth_list(mask);

        prod_table = P_mu_totalLSD(z_group, atm_depth, this_Rc, SPhi, mc, 'yes');

        p_neg_list(mask)  = prod_table.P_neg;
        p_fast_list(mask) = prod_table.P_fast;
    end
end

function Rc = lookup_Rc(t, times_table, Rc_table)
    idx = find(times_table >= t, 1, 'first');
    if ~isempty(idx)
        Rc = Rc_table(2,idx);
    else
        Rc = Rc_table(2,end);
    end
end