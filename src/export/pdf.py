#coding: utf-8 
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF

from dashboard.inputs.eye import Eye
from parameters.parameters import Parameters
from .google_sheet import send_data


class PDFGenerator:

	def __init__(self):
		self.pdf = PDFGenerator._initialize()
		self.left = 20
		self.top = 5
		self.interline = 4
		self.paragraph_interline = 6

	def generate(self, data, save=False):

		self._insert_logo()
		self._insert_header(data['demographics'])
		self._insert_etao(data["eTAO"])
		self._insert_surgery_information(data["surgery"])
		if data["report_type"] == 'OCULAR_DRYNESS':
			self._insert_dryness(data['ocular_dryness'])
		self._insert_eyes_report(data["right_eye"], data["left_eye"])
		if data["report_type"] == 'OCULAR_DRYNESS':
			self._insert_therapeutic_suggestions(data["recommendations"])
		else:
			self._insert_recommandations(data['eTAO'])
		self._insert_footer()

		self._display_button(data, save)



	@staticmethod
	def _initialize():

		pdf = FPDF()
		pdf.add_page()
		pdf.add_font(family="DejaVu", fname="static/fonts/DejaVu/DejaVuSans.ttf", uni=True)
		pdf.set_font("DejaVu", size=16)

		return pdf

	def _insert_logo(self):
		self.pdf.image("static/img/logo_clinique.png", x=120, y=self.top, h=40, type="png")
		self.top += 45

	def _insert_header(self, demographics):

		# Get data
		self.pdf.set_font_size(13)
		naming = Parameters.sex_to_naming(demographics['sex'])
		first_name = demographics['first_name'].capitalize()
		last_name = demographics['last_name'].upper()

		exam_date = demographics['exam_date']
		birthday = demographics['birthday']
		age = (exam_date - birthday).days/365.25

		# Set logo and title
		self.pdf.image("static/img/logo.png", x=self.left, y=self.top-16, h=30, type="png")

		self.pdf.set_font_size(19)
		self.pdf.text(self.left, 26, Parameters.text("PDF_REPORT", capitalize=False))
		self.top += 20

		# Set patient
		self.pdf.set_font_size(14)
		txt = f'{naming} {first_name} {last_name} - {int(np.floor(age))} ' + Parameters.text("AGE")
		texts = textwrap.wrap(txt, width=30)
		for txt in texts:
			self.pdf.text(self.left, self.top, txt)
			self.top += self.interline + 3
		self.top += 1

		# Set date
		self.pdf.set_font_size(11)
		date = f"{Parameters.text('PDF_REALIZATION')}  {exam_date.strftime('%d/%m/%Y')}"
		self.pdf.text(self.left, self.top, date)
		self.top += self.interline + 16



	def _insert_eyes_report(self, right_eye, left_eye):


		self.paragraph_interline = 2

		# eTAO - value
		for side, results in [('RIGHT', right_eye), ('LEFT', left_eye)]:
			# Add header
			header = Eye.get_eye_header(side)
			self.pdf.set_font_size(12)
			self._insert_new_paragraph(header)
			self.pdf.set_font_size(9)

			for letter in 'eTAO':
				color = results[letter]
				text = Parameters.get_eye_recommendation(letter, color)
				text = "\t- " + text
				self._insert_new_paragraph(text)
			self.top += 5

	def _insert_etao(self, eTAO):

		# eTAO Score
		self.pdf.set_font_size(19)
		self.pdf.set_text_color(229, 24, 24)
		text = f"{Parameters.text('PDF_ETAO_SCORE', capitalize=False)} : {eTAO:.2f}"
		self._insert_new_paragraph(text)
		self.pdf.set_text_color(0, 0, 0)
		self.top += 10


		img = Parameters.get_img_path('etao')
		self.pdf.image(img, x=self.left-5, y=self.top-15, h=20, type="png")

		img = Parameters.get_img_path('main_barplot')
		height = 74
		self.pdf.image(img, x=self.left + 100, y=self.top-70, h=height, type="png")

		self.top += 16



		#pdf.image(Parameters.get_img_path("etao"), x=10, y=70, h=17, type="png")
		#pdf.image(Parameters.get_img_path("main_barplot"), x=140, y=40, h=70, type="png")

	def _insert_dryness(self, ocular_dryness):

		# Header
		self.pdf.set_font_size(13)
		self._insert_new_paragraph(Parameters.text('DRYNESS_HEADER'))
		self.pdf.set_font_size(9)
		self.top -= 3


		# Ocular dryness
		int = ocular_dryness['intensity']
		txt = f"\t{Parameters.text('PDF_DRYNESS_INTENSITY')} : {int}/10. "
		if int == 0:
			txt += Parameters.get_intensity_recommendation("NONE")
		elif int < 6:
			txt += Parameters.get_intensity_recommendation("MILD")
		else:
			txt += Parameters.get_intensity_recommendation("SEVERE")

		self._insert_new_paragraph(txt, width=120)

		if int == 0:
			return

		fre = ocular_dryness['frequency']
		txt = f"{Parameters.text('PDF_FREQUENCY')} : {fre}/10. "
		if fre < 6:
			txt += Parameters.text('PDF_FREQUENCY_EXPLANATION_MILD')
		else:
			txt += Parameters.text('PDF_FREQUENCY_EXPLANATION_SEVERE')

		self._insert_new_paragraph(txt)

	def _insert_surgery_information(self, surgery):
		# Header
		self.pdf.set_font_size(13)
		self._insert_new_paragraph(Parameters.text("CONTEXT"))
		self.top -= 3
		self.pdf.set_font_size(9)

		text = []
		if surgery["lasik"]:
			text.append(Parameters.text("LASIK"))
		if surgery["iso"]:
			text.append(Parameters.text("ISOTRETINOIN"))
		if surgery["blepharo"]:
			text.append(Parameters.text("BLEPHAROPLASTY"))

		if len(text) == 0:
			text = f"\t{Parameters.text('PDF_SURGERY_INFORMATION_NO', capitalize=False)}"
		else:
			text = ', '.join(text) + '.'

		self._insert_new_paragraph(text, width=120)
		self.top += 3


	def _insert_therapeutic_suggestions(self, recommendations):
		# Header
		self.pdf.set_font_size(13)
		self._insert_new_paragraph(Parameters.text('RECOMMENDATIONS'))
		self.pdf.set_font_size(9)

		texts = []

		# Light
		if recommendations['light'] != 0:
			texts.append(f'\t- {recommendations["light"]} {Parameters.text("PDF_LIGHT", capitalize=False)}')
		# QMR
		if recommendations['QMR'] != 0:
			texts.append(f'\t- {recommendations["QMR"]} {Parameters.text("PDF_QMR", capitalize=False)}')
		# Lipiflow
		if recommendations['lipiflow'] != 0:
			texts.append(f'\t- {recommendations["lipiflow"]} {Parameters.text("PDF_LIPIFLOW", capitalize=False)}')
		# Lubricants
		if recommendations['lubricant']:
			texts.append(f'\t- {Parameters.text("PDF_LUBRICANT", capitalize=False)}')

		# Append
		if len(texts) == 0:
			texts.append(f'\t {Parameters.text("PDF_NO_RECOMMENDATION")}')

		for txt in texts:
			self._insert_new_paragraph(txt)

	def _insert_recommandations(self, eTAO):
		# Header
		self.pdf.set_font_size(13)
		self._insert_new_paragraph(Parameters.text("PDF_RECOMMENDATIONS"))
		self.pdf.set_font_size(9)

		texts = []

		if eTAO >= 2.5:
			texts.append(f"\t -{Parameters.text('PDF_RECOMMENDATION_LASIK')}")
		if eTAO >= 4.25:
			texts.append(f"\t -{Parameters.text('PDF_RECOMMENDATION_IMPLANTS')}")
		if eTAO >= 5.5:
			texts.append(f"\t -{Parameters.text('PDF_RECOMMENDATION_LENS')}")
		if eTAO >= 6:
			texts.append(f"\t -{Parameters.text('PDF_RECOMMENDATION_TOXICITY')}")

		# Append
		if len(texts) == 0:
			texts.append(f'\t {Parameters.text("PDF_NO_RECOMMENDATION")}')

		for txt in texts:
			self._insert_new_paragraph(txt)

	def _display_button(self, data, save):

		demographics = data['demographics']
		file_name = "CR__" + demographics["last_name"] + "_" + demographics["first_name"] + ".pdf"

		on_click = send_data if save else lambda x: x
		st.download_button(label=Parameters.text("GENERATE_REPORT"),
						   	data=bytes(self.pdf.output()),
						   file_name=file_name,
						   mime='application/octet-stream',
						   on_click=on_click,
						   args=(data,))

	def _insert_new_paragraph(self, text, width=100):
		texts = textwrap.wrap(text, width=width)
		for text in texts:
			self.pdf.text(self.left, self.top, text)
			self.top += self.interline
		self.top += self.paragraph_interline


	def _insert_footer(self):
		line_1 = "Institut Ophtalmologique de l'Œil Sec du Professeur DIGHIERO"
		line_2 = "96 bis Grande Rue - 77630 Barbizon - France"

		self.pdf.set_text_color(4, 61, 93)
		self.pdf.set_font_size(11)
		self.pdf.text(self.left + 24, 284, line_1)
		self.pdf.text(self.left + 40, 289, line_2)



	# OLD
	@staticmethod
	def save_recommandation(data, pdf):
		pdf.set_font_size(12)
		reco = data["recommandation"]
		reco = reco.split("-")
		for i, r in enumerate(reco):
			pdf.text(10, 100+i*5, r[1:-1])

	@staticmethod
	def save_eye(side, data, pdf):

		pdf.set_font_size(14)

		x_align = 10
		y_align = 150 if side == "right" else 220

		pdf.text(x_align, y_align-10, Parameters.get_text("eye", eye=side))


		pdf.set_font_size(10)

		eye_txt = data[f"eye_{side}_txt"]
		eye_colors = data[f"eye_{side}_colors"]
		iter_ = 0

		for txt, first_letter in zip(eye_txt, eye_colors):

			txt = txt[1:]

			pdf.text(x_align+1, y_align+iter_*6, txt)

			if first_letter == "G":
				r, g, b = Parameters.COLORS_RGB["green"]
			elif first_letter == "O":
				r, g, b = Parameters.COLORS_RGB["orange"]
			elif first_letter == "R":
				r, g, b = Parameters.COLORS_RGB["red"]
			elif first_letter == "W":
				r, g, b = Parameters.COLORS_RGB["grey"]
			else:
				ValueError("Error in the save_eye function")

			pdf.set_fill_color(r=r, g=g, b=b)
			pdf.circle(x=x_align, y=y_align+iter_*6-3.5, r=5, style="F")

			iter_ += 1


		### Save image
		pdf.image(Parameters.get_img_path(f'{side}_barplot'), x=x_align+100, y=y_align-20, h=50, type="png")

