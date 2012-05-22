
CLASS_CHOICES = (
    ('kind','Kindergarten'),
    ('1st','1st grade'),
    ('2nd','2nd grade'),
    ('3rd','3rd grade'),
    ('4th','4th grade'),
    ('5th','5th grade'),
    ('alum','Alumni'),    
    ('fut','Future'),        
)


CREDIT_TYPE_CHOICES = (
    ('partpar','Participating Parent'),
    ('aidsub','Aid Substitute'),
    ('teachsub','Teacher Substitute'),     
    ('incorbil','Incorrect Billing'),                     
    ('board','Board'),    
    ('housekp','Extra Housekeeping'),    
)

OBLIGATION_TYPE_CHOICES = (
    ('mbsmtg','Membership Meeting'),
    ('maint','Maintenance/Work Party'),
    ('fundrais','Fundraising'),    
    ('fldtrp','Field Trip'),
    ('oblscrp1','Annual Obligation/Scrip (1 child enrolled)'),    
    ('oblscrp2','Annual Obligation/Scrip (2 children enrolled)'),
    ('housekpg','Housekeeping'),
    ('cmt_coop','Committee/Co-op Job'),
)

READER_TYPE_CHOICES = (
    ('morn','Morning Reader'),
    ('aft','Afternoon Reader'),
    ('na','N/A (Kindergarten)'),
)

# Daycare is subject to financial aid post-processing, 
# so we separate it out from other charge types.
# When adding new charge type choices, you must explicitly make sure their shortcodes
# are also included in the main itaco views.py and also in the billing summary

CHARGE_TYPE_CHOICES = (
    ('hrdc','Hourly Regular Daycare'),
    ('meal','Meal Expense'),        
    ('pavdc','Vacation Daycare'),
    ('edc1','Event Daycare Flat Fee - 1 Child'),
    ('edc2','Event Daycare Flat Fee - 2 Child'),
    ('edc3','Event Daycare Flat Fee - 3 Child'),
    ('dclpu','Daycare Late Pickup'),            
    ('mshc','Missed Housecleaning'),
    ('mmh','Missed Maintenance'),
    ('mfrsg','Missed Fundraising'),
    ('mftr','Missed Fieldtrip'),
    ('mmtg','Missed Meeting'),        
    ('adj','Misc Adjustments'),
)



UNIT_CHOICES = (
    ('units','Units'),
    ('hours','Hours'),
    ('dollars','Dollars'),          
)


# 
# LIST_EXTRAS = (
#     ('second','second'),
#     ('first','first'),
#     ('fifth','fifth'),
#     ('third','third'),
#     ('fourth','fourth'),
#     ('kindergarten','kindergarten'),
#     ('board','board'),
#     ('first-nomail','first-nomail'),
#     ('teachers','teachers'),
#     ('everyone','everyone'),
#     ('executivecom','executivecom'),
#     ('alumni','alumni'),
#     ('participation','participation'),
#     ('twothree','twothree'),
#     ('fourfive','fourfive'),
#     ('teachers-nomail','teachers-nomail'),
#     ('board-nomail','board-nomail'),
#     ('twothree-nomail','twothree-nomail'),
#     ('fourfive-nomail','fourfive-nomail'),
#     ('second-nomail','second-nomail'),
#     ('third-nomail','third-nomail'),
#     ('fourth-nomail','fourth-nomail'),
#     ('fifth-nomail','fifth-nomail'),
#     ('kindergarten-nomail','kindergarten-nomail'),
#     ('executivecom-nomail','executivecom-nomail'),
#     ('participation-nomail','participation-nomail'),
#     ('everyone-nomail','everyone-nomail'),
# )

# Credit units doesn't have help text - we enter units automatically depending on the charge type selected.
OBL_UNITS_HELP_TEXT='<strong>Please use the following amounts when entering obligations:</strong><br />       Membership Meeting: 1 unit per meeting<br />        Maintenance/Work Party: Number of hours<br />        Fundraising: Number of hours<br />        Field Trip: Enter 1 unit per trip; partial credits OK e.g. .5 for driving halfway or .25 for BART pickup<br />        Annual Obligation/Scrip: Number of dollars<br />        Housekeeping: Enter 1 unit per cleaning<br />        Committee/Co-op Job: Enter 1 unit per job'
CREDIT_UNITS_HELP_TEXT='<strong>Please use the following units when entering credits. iTaco will convert to dollars automatically:</strong><br />         Board: DOLLARS<br />       Participating parent: HOURS <br /> Extra housekeeping: Hours (Note this is NOT the same as regular obligation housekeeping)<br />        Aid substitute: HOURS<br />   Teacher substitute: Hours<br />'
CHARGE_AMT_HELP_TEXT='<strong>Please enter amounts in the following units:</strong><br />Hourly regular day care, drop-in hourly daycare, pre-arranged vacation daycare: HOURS (e.g. 2.5)<br />Meal Expense: DOLLARS (K: Pizza=3,Bread=1; 1-5: Pizza=5,Bread=2)<br />Event daycare flat-fee: Select the number of children from the dropdown, and enter &quot;1&quot; for the amount, regardless the number of hours.<br />Daycare late pickup: Enter number of MINUTES after 6 p.m. that child was picked up (e.g. 37).<br />Missed housecleaning: Always enter &quot;1&quot; for the amount.<br />Missed maintenance: Enter number of HOURS (e.g. 1.5 or 3)<br />Missed fundraising: Always enter &quot;1&quot; for the amount.<br />Missed fieldtrip: Always enter &quot;1&quot; for the amount.<br />Missed meeting: Always enter &quot;1&quot; for the amount.<br />Misc adjustments: DOLLARS (e.g. 48.25)'
