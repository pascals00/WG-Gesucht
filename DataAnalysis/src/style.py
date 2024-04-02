from IPython.display import display, HTML

def centre_output():
    return display(HTML("""
<style>
    .output_png img {
        display: block;
        margin: auto;
    }
</style>
"""))


def display_as_table(df):
    df_html = df.to_html()
    scrollable_table = f'<div style="overflow-x:auto;">{df_html}</div>'
    return display(HTML(scrollable_table))

