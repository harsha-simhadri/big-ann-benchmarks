
# NeurIPS 2025

This README contains instructions so that you can modify/generate the neurips2025 poster.

I used react/html to generate the poster, and not Latex.

# Why React/HTML ?

Unfortunately, I had to generate the poster quickly due to a tight venue deadline.

I was more comfortable with react than LaTex, given the quick turnaround time and nearly everyone was on Thanksgiving vacation.

# Instructions

* Install the nodejs react tools on your system ( I used brew on MacOS ).
* Install the following packages:
  * tailwindcss 3
  * lucide-react
* cd into gen_poster/
* launch via 'npm start' and browse to the server url it emits (I used Chrome)
* make sure the poster loads correctly
* right-click the site and select the print
* create a new print setting with these dimensions:
  * width 48 inches
  * height 36 inches
  * no margins
* select print to PDF (1st page only( and save
* open the PDF and make sure the content is not clipped
