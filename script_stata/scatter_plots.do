clear all
set more off

*gen prod_file = "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_talking_3months_intervals_seg.csv"
*gen talking_file = "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_talked_3months_intervals_seg.csv"
*gen talked_file = "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_productivity_3months_intervals_seg.csv"


*import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_talking_1month_intervals_seg.csv", encoding(ISO-8859-1)
import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_talking_3months_intervals_seg.csv", encoding(ISO-8859-1)
scatter talkings time_interval, xtitle("time in month") ytitle("amount of talking to others within wikiprojects")
*graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/talkings_overtime.png", replace
graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/talkings_overtime3.png", replace

clear all

*import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_talked_1month_intervals_seg.csv", encoding(ISO-8859-1)
import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_talked_3months_intervals_seg.csv", encoding(ISO-8859-1)
scatter talkings time_interval, xtitle("time in month") ytitle("amount of being talked from others within wikiprojects")
*graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/talkeds_overtime.png", replace
graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/talkeds_overtime3.png", replace

clear all

*import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_productivity_1month_intervals_seg.csv", encoding(ISO-8859-1)
import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/lng_revs_amount_productivity_3months_intervals_seg.csv", encoding(ISO-8859-1)

import delimited "/Users/bobo/Documents/wikipedia_user_dropout/data/analysis_data/script_lng_revs_amount_productivity_3months_intervals_seg.csv", encoding(ISO-8859-1)

scatter productivity time_interval, xtitle("time in month") ytitle("editor productivity within wikiprojects"), if tcount >= 0
*graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/productivity_overtime.png", replace
graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/productivity_overtime3.png", replace


scatter productivity tcount, xtitle("time in month") ytitle("editor productivity within wikiprojects"), if tcount >= 0 & productivity < 20000
graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/productivity_overtime3_updated.png", replace

scatter productivity tcount, xtitle("Time Period in 3 Months") ytitle("Editor Productivity within Wikiprojects After Joining"), if tcount >= 0 & productivity < 12000
scatter productivity tcount, xtitle("Time Period in 3 Months") ytitle("Editor Productivity"), if tcount >= 0 & productivity < 12000 || lfit productivity tcount
graph export "/Users/bobo/Documents/wikipedia_user_dropout/plots/productivity_overtime3_updated12k.png", replace
