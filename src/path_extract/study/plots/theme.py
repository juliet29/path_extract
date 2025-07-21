import altair as alt

CLEARVIEW = "ClearviewText"
FONT = f'{CLEARVIEW}, system-ui, -apple-system, BlinkMacSystemFont, ".SFNSText-Regular", sans-serif'
FONT_SIZE = 18
LABEL_FONT_SIZE = 10
FONT_COLOR = "#161616"
LABEL_COLOR = "#525252"
DEF_WIDTH = 350
DEF_HEIGHT = 280


category_pallete = ["#5c898a", "#022B3A", "#52AA5E", "#976391", "#F7996E"]


@alt.theme.register("scape", enable=True)
def scape() -> alt.theme.ThemeConfig:
    return {
        "config": {
            "view": {
                "width": DEF_WIDTH,
                "height": DEF_HEIGHT,
            },
            "axis": {
                "labelColor": LABEL_COLOR,
                "labelFontSize": LABEL_FONT_SIZE,
                "labelFont": FONT,
                "labelFontWeight": 400,
                "titleColor": FONT_COLOR,
                "titleFontWeight": 600,
                "titleFontSize": LABEL_FONT_SIZE,
            },
            "axisX": {"titlePadding": 10},
            "axisY": {"titlePadding": 2.5},
            "text": {"font": FONT, "fontSize": FONT_SIZE, "fontWeight": "bold"},
            "range": {
                "ordinal": {"scheme": "teals"},
                "category": category_pallete,
                "sequential": {"scheme": "teals"},
                "diverging": {"scheme": "brownbluegreen"},
            },  # type: ignore
            "legend": {"labelFont": FONT, "labelFontSize": LABEL_FONT_SIZE},
        }
    }
