# import altair as alt

# CLEARVIEW = "ClearviewText"
# FONT = f'{CLEARVIEW}, system-ui, -apple-system, BlinkMacSystemFont, ".SFNSText-Regular", sans-serif'
# FONT_SIZE = 16

# axis = alt.AxisConfig(
#     {
#         "labelColor": "#525252",
#         "labelFontSize": FONT_SIZE,
#         "labelFont": FONT,
#         "labelFontWeight": 400,
#         "titleColor": "#161616",
#         "titleFontWeight": 600,
#         "titleFontSize": FONT_SIZE,
#         "grid": True,
#         "gridColor": "#e0e0e0",
#         "labelAngle": 0,
#     }
# ).to_dict()


# @alt.theme.register("scape", enable=True)
# def scape() -> alt.theme.ThemeConfig:
#     # Typography
#     font = CLEARVIEW
#     # At Urban it's the same font for all text but it's good to keep them separate in case you want to change one later.
#     labelFont = CLEARVIEW
#     sourceFont = CLEARVIEW
#     # Axes
#     axisColor = "#000000"
#     gridColor = "#DEDDDD"
#     markColor = ("#1696d2",)
#     # Colors
#     main_palette = [
#         "#1696d2",
#         "#d2d2d2",
#         "#000000",
#         "#fdbf11",
#         "#ec008b",
#         "#55b748",
#         "#5c5859",
#         "#db2b27",
#     ]
#     sequential_palette = [
#         "#cfe8f3",
#         "#a2d4ec",
#         "#73bfe2",
#         "#46abdb",
#         "#1696d2",
#         "#12719e",
#     ]

#     return {
#         "config": {
#             "title": {},
#             "axis": {
#                 "labelColor": "#525252",
#                 "labelFontSize": FONT_SIZE,
#                 "labelFont": FONT,
#                 "labelFontWeight": 400,
#                 "titleColor": "#161616",
#                 "titleFontWeight": 600,
#                 "titleFontSize": FONT_SIZE,
#                 "grid": True,
#                 "gridColor": "#e0e0e0",
#                 "labelAngle": 0,
#             },
#             "axisX": {"titlePadding": 10},
#             "axisY": {"titlePadding": 2.5},
#             "legend": {},
#             "range": {"category": main_palette, "diverging": sequential_palette},
#         }
#     }
