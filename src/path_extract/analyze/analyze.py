from path_extract.extract.extract import extract_data
from path_extract.paths import SAMPLE_HTML, BASE_PATH
from path_extract.constants import ClassNames, Headings
import polars as pl 
from rich import print as rprint
import altair as alt 



def clean_df(df: pl.DataFrame):
	# TODO check dataframe columns.. use set comaparison//
	# set([i.name for i in ClassNames])

	d = df.filter(pl.col(ClassNames.VALUE.name) >0) # strong filter for right now where dont have valid data.. 
	

	# just want to see carbon impact.. 
	d = df.filter(pl.col(ClassNames.SECTION.name) ==  Headings.CARBON_IMPACT.value)
	# rprint(d)

	return d

	# group by category 


def plot_elements_by_category(df: pl.DataFrame, title="", renderer="browser"):
	alt.renderers.enable(renderer)
	# chart = alt.Chart(df).mark_bar().encode(
    # x=ClassNames.ELEMENT.name,
    # y=ClassNames.VALUE.name, color=ClassNames.CATEGORY.name)
	# chart.show()
	chart = alt.Chart(df, title=title).mark_bar().encode(
    x=alt.X(ClassNames.CATEGORY.name).title("Category Names"),
    y=alt.Y(f"sum({ClassNames.VALUE.name})").title("Equivalent Carbon Emissions [kg-Co2-e]"), color=ClassNames.ELEMENT.name, tooltip=ClassNames.ELEMENT.name)
	chart.show()
	


if __name__ == "__main__":
	# alt.renderers.enable("browser")
	# uncomment below
	df = extract_data(SAMPLE_HTML)
	df2 = clean_df(df)
	plot_elements_by_category(df2)

	res = df2.group_by(ClassNames.CATEGORY.name, maintain_order=True).agg(ClassNames.ELEMENT.name)
	rprint(res)

	df2.write_csv(file = BASE_PATH / "test.csv")
 