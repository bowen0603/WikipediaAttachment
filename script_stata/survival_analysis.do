clear all
set more off

import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/results_dvs_cvs_ivs_encoded_final.csv", encoding(ISO-8859-1)

** harzard rate: the probablity of having the event (withdrawal)

** log transform all variables except the cos_sim
gen ln_cv_wp_age = ln(cv_wp_age+1) / ln(2)
gen ln_cv_wp_member_size = ln(cv_wp_member_size+1) / ln(2)
gen ln_cv_wp_art_size = ln(cv_wp_art_size+1) / ln(2)
gen ln_cv_user_tenure = ln(cv_user_tenure+1) / ln(2)
gen ln_cv_prior_edits = ln(cv_prior_edits+1) / ln(2)

gen ln_iv_amount_talked = ln(iv_amount_talked+1) / ln(2)
gen ln_iv_amount_talking = ln(iv_amount_talking+1) / ln(2)
gen ln_iv_workload = ln(cv_workload+1) / ln(2)


* standardize cvs and ivs
egen lns_cv_wp_age = std(ln_cv_wp_age)
egen lns_cv_wp_member_size = std(ln_cv_wp_member_size)
egen lns_cv_wp_art_size = std(ln_cv_wp_art_size)
egen lns_cv_user_tenure = std(ln_cv_user_tenure)
egen lns_cv_prior_edits = std(ln_cv_prior_edits)

egen s_iv_cos_sim = std(iv_cos_sim)
egen lns_iv_amount_talking = std(ln_iv_amount_talking)
egen lns_iv_workload = std(ln_iv_workload)

* interaction terms
gen cosim_amtlking = s_iv_cos_sim*lns_iv_amount_talking
gen cosim_workload = s_iv_cos_sim*lns_iv_workload
gen workload_talking = lns_iv_amount_talking*lns_iv_workload


gen iv_active_duration_year = iv_active_duration / 12
global time iv_active_duration_year
global event dv_withdrawal
global xlist s_iv_cos_sim lns_iv_amount_talking 
global clist lns_cv_wp_age lns_cv_wp_member_size lns_cv_wp_art_size lns_cv_user_tenure lns_cv_prior_edits lns_iv_workload
global ilist cosim_amtlking cosim_workload workload_talking


egen median_identity = median(s_iv_cos_sim)
egen median_bonds = median(lns_iv_amount_talking)

gen user_group = ""
replace user_group = "Low Identity & Low Bonds" if s_iv_cos_sim < median_identity & lns_iv_amount_talking <= median_bonds
replace user_group = "Low Identity & High Bonds" if s_iv_cos_sim < median_identity & lns_iv_amount_talking > median_bonds
replace user_group = "High Identity & Low Bonds" if s_iv_cos_sim > median_identity & lns_iv_amount_talking <= median_bonds
replace user_group = "High Identity & High Bonds" if s_iv_cos_sim > median_identity & lns_iv_amount_talking > median_bonds


gen identity_group = ""
stset $time, failure($event)
global group identity_group

replace identity_group = "Low Identity" if s_iv_cos_sim <= median_identity
replace identity_group = "High Identity" if s_iv_cos_sim > median_identity
global group identity_group
sts graph, by($group) xtitle("Years Since Joining the Project")  ytitle("Cumulative Survival") title("Survival Analysis") legend(textwidth(40)) name(p1)
sts graph, by($group) xtitle("Years Since Joining the Project")  ytitle("Cumulative Survival") legend(textwidth(40)) name(p1)

gen bond_group = ""
replace bond_group = "Low Bonds" if lns_iv_amount_talking <= median_bonds
replace bond_group = "High Bonds" if lns_iv_amount_talking > median_bonds
global group bond_group
sts graph, by($group) xtitle("Years Since Joining the Project")  ytitle("Cumulative Survival") title("Survival Analysis") legend(textwidth(40)) name(p2)
sts graph, by($group) xtitle("Years Since Joining the Project")  legend(textwidth(40)) name(p2)

graph combine p1, p2, title("Survival Analysis")
graph drop p1, p2

stset $time, failure($event)

* sts graph, hazard xlabel(0(1)14) xtitle("analysis time (in year)")
* sts graph, cumhaz xlabel(0(1)14) xtitle("analysis time (in year)")

global group user_group
sts graph, by($group) xtitle("Years Since Joining the Project")  ytitle("Cumulative Survival") title("Survival Analysis") legend(textwidth(40))




* reset the time period in month
global time iv_active_duration
stset $time, failure($event)

* Exponential regression coefficients and harzard rates

streg $clist, dist(exponential)
est sto model1

streg $clist $xlist, dist(exponential)
est sto model2
lrtest model1 model2

streg $clist $xlist $ilist, dist(exponential)
est sto model3
lrtest model2 model3

stmixed $clist || nwikiproject:, dist(exponential)


stmixed $clist $xlist || nwikiproject:, dist(exponential)
est sto model2
lrtest model1 model2

stmixed $clist $xlist $ilist || nwikiproject:, dist(exponential)
est sto model3
lrtest model2 model3

 * explanation on hazard ratio: if > 1, one unit increase on the iv, % increase on the hazard rate.
* < 1, positive effect
/*
pos - lower duration
neg - higher duration

hazard ratio
> 1 increase % higher hazard rate
high hazard rate => more stay
low hazard rate => more leave
*/
