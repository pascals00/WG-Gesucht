from IPython.display import display, HTML
import matplotlib.pyplot as plt

def centre_output():
    return display(HTML("""
<style>
    .output_png img {
        display: block;
        margin: auto;
    }
</style>
"""))


def save_reg_results(ind_var, dep_var, model): 
    # Create a figure with matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))

    # Capture the summary as a string
    summary = model.summary().as_text()

    # Add the summary text to the plot
    ax.text(0.01, 0.05, summary, fontfamily='monospace', fontsize=12, verticalalignment='bottom')

    # Hide the axes
    ax.axis('off')

    # Adjust layout to make room for the text
    plt.tight_layout()

    # Save the figure to a file
    save_path = f'data/output/priceDeterminants/{ind_var}&{dep_var}Regression.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def display_as_table(df):
    df_html = df.to_html()
    scrollable_table = f'<div style="overflow-x:auto;">{df_html}</div>'
    return display(HTML(scrollable_table))



