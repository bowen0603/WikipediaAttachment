clear all
set more off

import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_results_3months.csv", encoding(ISO-8859-1)

** fix the problem in the data
replace iv_wp_tenure = 0 if iv_wp_tenure < 0
replace iv_wp_tenure = iv_wp_tenure / (3600*24*30)


corr dlt_bonds dlt_identity iv_wp_tenure iv_prior_edits iv_avg_mbr_tenure


gen ln_iv_prior_edits = ln(iv_prior_edits+1) / ln(2)

egen lns_iv_prior_edits = std(iv_prior_edits)
egen s_iv_wp_tenure = std(iv_wp_tenure)
egen s_mbr_tenure = std(iv_avg_mbr_tenure)

corr dlt_bonds dlt_identity lns_iv_prior_edits s_iv_wp_tenure s_mbr_tenure

* wikiproject is self encoded in the data // encode wikiproject, gen(nwikiproject)
xtset user_wp

xtreg dlt_bonds lns_iv_prior_edits s_iv_wp_tenure s_mbr_tenure
xtreg dlt_identity lns_iv_prior_edits s_iv_wp_tenure s_mbr_tenure

ttest dlt_bonds=0 if tcount <0
ttest dlt_bonds=0 if tcount >0
ttest dlt_identity =0 if tcount <0
ttest dlt_identity =0 if tcount >0
