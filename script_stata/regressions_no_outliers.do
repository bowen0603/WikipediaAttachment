clear all
set more off

import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/results_dvs_cvs_ivs_encoded_final.csv", encoding(ISO-8859-1)

* wikiproject is self encoded in the data // encode wikiproject, gen(nwikiproject)
xtset nwikiproject

** correlation between IVs
cor iv_cos_sim iv_amount_talked iv_amount_talking iv_max_talked iv_max_talking iv_member_talked iv_member_talking cv_prior_edits cv_wp_age cv_wp_member_size cv_user_tenure cv_wp_art_size cv_workload

** log transform all the standarize variables except the cos_sim
gen ln_cv_wp_age = ln(cv_wp_age+1) / ln(2)
gen ln_cv_workload = ln(cv_workload+1) / ln(2)
gen ln_cv_wp_member_size = ln(cv_wp_member_size+1) / ln(2)
gen ln_cv_wp_art_size = ln(cv_wp_art_size+1) / ln(2)
gen ln_cv_user_tenure = ln(cv_user_tenure+1) / ln(2)
gen ln_cv_prior_edits = ln(cv_prior_edits+1) / ln(2)

gen ln_iv_amount_talked = ln(iv_amount_talked+1) / ln(2)
gen ln_iv_amount_talking = ln(iv_amount_talking+1) / ln(2)
gen ln_iv_member_talked = ln(iv_member_talked+1) / ln(2)
gen ln_iv_member_talking = ln(iv_member_talking+1) / ln(2)
gen ln_iv_max_talked = ln(iv_max_talked+1) / ln(2)
gen ln_iv_max_talking = ln(iv_max_talking+1) / ln(2)

** standarize all the control and independent variables
egen lns_cv_wp_age = std(ln_cv_wp_age)
egen lns_cv_workload = std(ln_cv_workload)
egen lns_cv_wp_member_size = std(ln_cv_wp_member_size)
egen lns_cv_wp_art_size = std(ln_cv_wp_art_size)
egen lns_cv_user_tenure = std(ln_cv_user_tenure)
egen lns_cv_prior_edits = std(ln_cv_prior_edits)

egen s_iv_cos_sim = std(iv_cos_sim)

egen lns_iv_amount_talked = std(ln_iv_amount_talked)
egen lns_iv_amount_talking = std(ln_iv_amount_talking)
egen lns_iv_member_talked = std(ln_iv_member_talked)
egen lns_iv_member_talking = std(ln_iv_member_talking)
egen lns_iv_max_talked = std(ln_iv_max_talked)
egen lns_iv_max_talking = std(ln_iv_max_talking)

** regression on control variables
xtnbreg dv_productivity lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits, irr
xtnbreg dv_communication lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits, irr
xtnbreg dv_work_comm lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits, irr
xtnbreg dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits, irr


** check correlations between transferred IVs and CVs
corr lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits s_iv_cos_sim lns_iv_amount_talked lns_iv_amount_talking

** generate IV interaction terms
gen cosim_amtlked = s_iv_cos_sim*lns_iv_amount_talked
gen cosim_amtlking = s_iv_cos_sim*lns_iv_amount_talking
gen cosim_mbrtlked = s_iv_cos_sim*lns_iv_member_talked
gen cosim_mbrtlking = s_iv_cos_sim*lns_iv_member_talking
gen cosim_maxtlked = s_iv_cos_sim*lns_iv_max_talked
gen cosim_maxtlking = s_iv_cos_sim*lns_iv_max_talking


** check correlations
corr dv_productivity dv_communication dv_work_comm dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_amtlking cosim_amtlked

** regression with IV interaction terms - pairs of amounts of talks
xtnbreg dv_productivity lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_amtlking cosim_amtlked, irr, if dv_productivity < 5000
xtnbreg dv_communication lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_amtlking cosim_amtlked, irr, if dv_communication < 5000
xtnbreg dv_work_comm lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_amtlking cosim_amtlked, irr, if dv_work_comm < 5000
xtnbreg dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_amtlking cosim_amtlked, irr, if dv_coordination < 5000

** check correlations
corr dv_productivity dv_communication dv_work_comm dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_mbrtlking cosim_mbrtlked

** regression with IV interaction terms - pairs of member of talks
xtnbreg dv_productivity lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_member_talked lns_iv_member_talking s_iv_cos_sim cosim_mbrtlking cosim_mbrtlked, irr, if dv_productivity < 5000
xtnbreg dv_communication lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_member_talked lns_iv_member_talking s_iv_cos_sim cosim_mbrtlking cosim_mbrtlked, irr, if dv_communication < 5000
xtnbreg dv_work_comm lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_member_talked lns_iv_member_talking s_iv_cos_sim cosim_mbrtlking cosim_mbrtlked, irr, if dv_work_comm < 5000
xtnbreg dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_member_talked lns_iv_member_talking s_iv_cos_sim cosim_mbrtlking cosim_mbrtlked, irr, if dv_coordination < 5000

** check correlations
corr dv_productivity dv_communication dv_work_comm dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_amount_talked lns_iv_amount_talking s_iv_cos_sim cosim_maxtlking cosim_maxtlked

** regression with IV interaction terms - pairs of max of talks
xtnbreg dv_productivity lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_max_talked lns_iv_max_talking s_iv_cos_sim cosim_maxtlking cosim_maxtlked, irr, if dv_productivity < 5000
xtnbreg dv_communication lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_max_talked lns_iv_max_talking s_iv_cos_sim cosim_maxtlking cosim_maxtlked, irr, if dv_communication < 5000
xtnbreg dv_work_comm lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_max_talked lns_iv_max_talking s_iv_cos_sim cosim_maxtlking cosim_maxtlked, irr, if dv_work_comm < 5000
xtnbreg dv_coordination lns_cv_wp_age lns_cv_workload lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_max_talked lns_iv_max_talking s_iv_cos_sim cosim_maxtlking cosim_maxtlked, irr, if dv_coordination < 5000
