from matplotlib.backends.backend_pdf import PdfPages


def export_to_pdf(plt, file_name):
    with PdfPages(file_name) as pdf:
        pdf.savefig()  # save figure to pdf
        plt.close()
