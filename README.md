# GAM_elbrot_prediction
Here is the intermediate-final version of the code that works more or less file for the prediction of elbow rotation in 16 adult participants based on their spectral characteristics in specific vertices of M1 (based on MEG cluster permutation test at source level, with TFCE) 

Steps:

0-1. First step is to generate dataframes to run .qmd scripts. For this, you need files from orig_data/ and additional_files/ directories.
0-2. Using these files, you can modify dfs_for_r_in_M1_alpha_beta_short_for_git.py script (paths to files) and run it to generate dataframes for R.

1. If you're fine with already created using this .py script dataframes (they include data log-transformed for power and z-scored for power and beta volume variables), you can skip 0-1 and 0-2 steps and just download already existing dataframes from dataframes_zscored/ directory.
2. Use these dataframes (or others created with dfs_for_r_in_M1_alpha_beta_short_for_git.py script) to run
    - R_gam_M1_indvert_mult_models_zscored_superlet20_git_version.qmd
      or
    - R_gam_M1_indvert_mult_models_zscored_superlet20_allelbrots_git_version.qmd.
   The difference between the two is that the one containing 'allelbrots' doesn't exclude trials with large elbow rotations (there's a small number of such trials, and models are fitted worse with them; still, they might be interesting too, and the models' output is not that bad).

3. If you just want to see the result of R_gam_M1_indvert_mult_models_zscored_superlet20_git_version.qmd and/or R_gam_M1_indvert_mult_models_zscored_superlet20_allelbrots_git_version.qmd, see the corresponding .pdf files (.html didn't work properly for me):
   - R_gam_M1_diff_dfs_and_models_superlet20_prevmodels_logpower_zscored.pdf
     or
   - R_gam_M1_diff_dfs_and_models_superlet20_prevmodels_logpower_allelbrots_zscored.pdf
