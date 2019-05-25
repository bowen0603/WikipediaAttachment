clear all
set more off

import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/results_dvs_cvs_ivs_encoded_final.csv", encoding(ISO-8859-1)

* wikiproject is self encoded in the data // encode wikiproject, gen(nwikiproject)
xtset nwikiproject

** correlation between IVs and CVs
cor iv_cos_sim iv_amount_talked iv_amount_talking iv_max_talked iv_max_talking iv_member_talked iv_member_talking cv_prior_edits cv_wp_age cv_wp_member_size cv_user_tenure cv_wp_art_size cv_workload
** adding DVs
cor iv_cos_sim iv_amount_talked iv_amount_talking iv_max_talked iv_max_talking iv_member_talked iv_member_talking cv_prior_edits cv_wp_age cv_wp_member_size cv_user_tenure cv_wp_art_size cv_workload dv_coordination dv_productivity dv_withdrawal dv_work_comm 

** log transform all the standarize variables except the cos_sim
gen ln_cv_wp_age = ln(cv_wp_age+1) / ln(2)
gen ln_cv_wp_member_size = ln(cv_wp_member_size+1) / ln(2)
gen ln_cv_wp_art_size = ln(cv_wp_art_size+1) / ln(2)
gen ln_cv_user_tenure = ln(cv_user_tenure+1) / ln(2)
gen ln_cv_prior_edits = ln(cv_prior_edits+1) / ln(2)

gen ln_iv_workload = ln(cv_workload+1) / ln(2)
gen ln_iv_amount_talked = ln(iv_amount_talked+1) / ln(2)
gen ln_iv_amount_talking = ln(iv_amount_talking+1) / ln(2)
gen ln_iv_member_talked = ln(iv_member_talked+1) / ln(2)
gen ln_iv_member_talking = ln(iv_member_talking+1) / ln(2)
gen ln_iv_max_talked = ln(iv_max_talked+1) / ln(2)
gen ln_iv_max_talking = ln(iv_max_talking+1) / ln(2)

** standarize all the control and independent variables
egen lns_cv_wp_age = std(ln_cv_wp_age)
egen lns_cv_wp_member_size = std(ln_cv_wp_member_size)
egen lns_cv_wp_art_size = std(ln_cv_wp_art_size)
egen lns_cv_user_tenure = std(ln_cv_user_tenure)
egen lns_cv_prior_edits = std(ln_cv_prior_edits)

egen s_iv_cos_sim = std(iv_cos_sim)

egen lns_iv_workload = std(ln_iv_workload)
egen lns_iv_amount_talked = std(ln_iv_amount_talked)
egen lns_iv_amount_talking = std(ln_iv_amount_talking)
egen lns_iv_member_talked = std(ln_iv_member_talked)
egen lns_iv_member_talking = std(ln_iv_member_talking)
egen lns_iv_max_talked = std(ln_iv_max_talked)
egen lns_iv_max_talking = std(ln_iv_max_talking)

** correlations between control variables
corr lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload

** KEY RESULTS
* lns_cv_user_tenure and lns_cv_prior_edits are 0.74
* lns_cv_wp_age lns_cv_wp_member_size are 0.74

** correlation between CVs and IVs
corr lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload s_iv_cos_sim lns_iv_max_talking

** check correlations between transferred each pair of IVs with CVs
corr lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talked lns_iv_amount_talking lns_iv_workload
corr lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_member_talked lns_iv_member_talking lns_iv_workload
corr lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_max_talked lns_iv_max_talking lns_iv_workload

** check the collinearity between IVs and CVs
collin lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload s_iv_cos_sim lns_iv_amount_talking

** KEY RESULTS
* lns_iv_amount_talked and lns_iv_amount_talking is 0.79
* lns_iv_member_talked and lns_iv_member_talking is 0.79
* lns_iv_max_talked and lns_iv_max_talking is 0.74

** 
corr lns_iv_amount_talked lns_iv_amount_talking lns_iv_member_talked lns_iv_member_talking lns_iv_max_talked lns_iv_max_talking

** generate IV interaction terms
gen cosim_amtlking = s_iv_cos_sim*lns_iv_amount_talking
gen cosim_mbrtlking = s_iv_cos_sim*lns_iv_member_talking
gen cosim_workload = s_iv_cos_sim*lns_iv_workload
gen workload_talking = lns_iv_amount_talking*lns_iv_workload
gen workload_mbr = lns_iv_member_talking*lns_iv_workload

** grouped by below or above the median
gen bond_group = ""
gen identity_group = ""

egen median_identity = median(s_iv_cos_sim)
egen median_bonds = median(lns_iv_amount_talking)

replace identity_group = "Low Identity" if s_iv_cos_sim <= median_identity
replace identity_group = "High Identity" if s_iv_cos_sim > median_identity
graph bar dv_productivity, over(identity_group)

replace bond_group = "Low Bonds" if lns_iv_amount_talking <= median_bonds
replace bond_group = "High Bonds" if lns_iv_amount_talking > median_bonds
graph bar dv_productivity, over(bond_group)

** grouped by above and below one std of the mean
replace bond_group = ""
replace identity_group = ""

egen mean_identity = mean(s_iv_cos_sim)
egen mean_bonds = mean(lns_iv_amount_talking)

replace identity_group = "Identity - One SD Below Mean" if s_iv_cos_sim <= mean_identity-1
replace identity_group = "Identity - One SD Above Mean" if s_iv_cos_sim > mean_identity+1
graph bar dv_productivity, over(identity_group)

replace bond_group = "Bonds - One SD Below Mean" if lns_iv_amount_talking <= mean_bonds-1
replace bond_group = "Bonds - One SD Above Mean" if lns_iv_amount_talking > mean_bonds+1
graph bar dv_productivity, over(bond_group)

gen iv_cos_sim_non_zero = iv_cos_sim  + 0.001 
xtnbreg dv_productivity ln_cv_wp_age ln_cv_wp_member_size ln_cv_wp_art_size ln_cv_user_tenure ln_cv_prior_edits iv_cos_sim_non_zero  ln_iv_amount_talking ln_iv_workload, irr
margins iv_cos_sim, at(iv_cos_sim=.1409936)
** three models for each DV
* model 1: control variables; 
* model 2: control variables + main effects; 
* model 3: control variables + main effects + interaction terms;

** productivity
corr dv_productivity lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking

xtnbreg dv_productivity lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload, irr
est sto model1

xtnbreg dv_productivity lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload, irr
est sto model2
lrtest model1 model2

xtnbreg dv_productivity lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking, irr
est sto model3
lrtest model2 model3


** communication
/*
** not highly correlated .. but still cannot converge
xtnbreg dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits, irr
xtnbreg dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload, irr
xtnbreg dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking, irr
*/
cor dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_member_talking lns_iv_workload cosim_mbrtlking cosim_workload workload_mbr

xtnbreg dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits, irr
xtnbreg dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_member_talking lns_iv_workload, irr
xtnbreg dv_communication lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_member_talking lns_iv_workload cosim_mbrtlking cosim_workload workload_mbr, irr


cor dv_work_comm lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking
** work communication
xtnbreg dv_work_comm lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload, irr
est sto model1

xtnbreg dv_work_comm lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload, irr
est sto model2
lrtest model1 model2

* test the coefficient difference between the two IVs
test s_iv_cos_sim - lns_iv_amount_talking = 0

xtnbreg dv_work_comm lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking, irr
est sto model3
lrtest model2 model3


cor dv_coordination lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking
** coordination
xtnbreg dv_coordination lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload, irr
est sto model1

xtnbreg dv_coordination lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload, irr
est sto model2
lrtest model1 model2

xtnbreg dv_coordination lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talking lns_iv_workload cosim_amtlking cosim_workload workload_talking, irr
est sto model3
lrtest model2 model3
