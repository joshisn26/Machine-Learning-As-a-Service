from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class predictionForm(Form):
	id = StringField('ID')
	credit_score = StringField('Credit Score', validators=[DataRequired(message ="Please enter credit score")])	
	first_payment_date = StringField('First Payment Date', validators=[DataRequired(message ="Please enter a First Payment Date")])
	fthb_flag = StringField('First Time house Buyer flag', validators=[DataRequired(message ="Please enter a fthb flag")])
	matr_date = StringField('Maturity Date', validators=[DataRequired(message ="Please enter Maturity Date")])
	msa = StringField('METROPOLITAN STATISTICAL AREA (MSA)', validators=[DataRequired(message ="Please enter MSA")])
	mortage_insurance_pct = StringField('Mortgage insurance percentage', validators=[DataRequired(message ="Please enter a MI")])
	no_of_units = StringField('No. of units', validators=[DataRequired(message ="Please enter number of units")])
	occupancy_status = StringField('Occupancy status', validators=[DataRequired(message ="Please enter Occupancy status")])
	cltv = StringField('ORIGINAL COMBINED LOAN-TO-VALUE', validators=[DataRequired(message ="Please enter cltv")])
	dti_ratio = StringField('ORIGINAL DEBT-TO-INCOME (DTI) RATIO', validators=[DataRequired(message ="Please enter DTI ratio")])
	original_upb = StringField('UPB', validators=[DataRequired(message ="Please enter UPB")])
	submit = SubmitField("Get interest rate")