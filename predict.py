from cog import BasePredictor, Input, Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import tempfile

class Predictor(BasePredictor):
    def predict(
        self,
        mode: str = Input(
            description="Number of circles in the Venn diagram",
            choices=["2", "3"],
            default="3"
        ),
        left_label: str = Input(
            description="Label for the left circle",
            default="Set A"
        ),
        middle_label: str = Input(
            description="Label for the middle circle (only for 3-circle mode)",
            default="Set B"
        ),
        right_label: str = Input(
            description="Label for the right circle",
            default="Set C"
        ),
        # 2-circle mode inputs
        left_only_2: str = Input(
            description="[2-circle mode] Terms only in left circle (comma or newline separated)",
            default=""
        ),
        right_only_2: str = Input(
            description="[2-circle mode] Terms only in right circle (comma or newline separated)",
            default=""
        ),
        both: str = Input(
            description="[2-circle mode] Terms in both circles (comma or newline separated)",
            default=""
        ),
        # 3-circle mode inputs
        left_only: str = Input(
            description="[3-circle mode] Terms only in left circle (comma or newline separated)",
            default=""
        ),
        middle_only: str = Input(
            description="[3-circle mode] Terms only in middle circle (comma or newline separated)",
            default=""
        ),
        right_only: str = Input(
            description="[3-circle mode] Terms only in right circle (comma or newline separated)",
            default=""
        ),
        left_middle: str = Input(
            description="[3-circle mode] Terms in left AND middle circles (comma or newline separated)",
            default=""
        ),
        left_right: str = Input(
            description="[3-circle mode] Terms in left AND right circles (comma or newline separated)",
            default=""
        ),
        middle_right: str = Input(
            description="[3-circle mode] Terms in middle AND right circles (comma or newline separated)",
            default=""
        ),
        all_three: str = Input(
            description="[3-circle mode] Terms in all three circles (comma or newline separated)",
            default=""
        ),
        export_format: str = Input(
            description="Output format for the diagram",
            choices=["png", "svg"],
            default="png"
        ),
        dpi: int = Input(
            description="DPI for PNG output (ignored for SVG)",
            default=300,
            ge=72,
            le=600
        )
    ) -> Path:
        """Generate a Venn diagram with 2 or 3 circles, custom labels, and terms"""
        
        if mode == "2":
            return self._create_2_circle(
                left_label, right_label,
                left_only_2, right_only_2, both,
                export_format, dpi
            )
        else:
            return self._create_3_circle(
                left_label, middle_label, right_label,
                left_only, middle_only, right_only,
                left_middle, left_right, middle_right, all_three,
                export_format, dpi
            )
    
    def _create_2_circle(self, left_label, right_label,
                        left_only, right_only, both,
                        export_format, dpi):
        """Create a 2-circle Venn diagram"""
        left_label = left_label or "Set A"
        right_label = right_label or "Set B"
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        v = venn2(
            subsets=(1, 1, 1),
            set_labels=(left_label, right_label),
            ax=ax
        )
        
        colors = ['#ff9999', '#99ccff', '#ffcccc']
        
        if v.patches:
            for i, patch in enumerate(v.patches):
                if patch:
                    patch.set_alpha(0.4)
                    if i < len(colors):
                        patch.set_color(colors[i])
        
        if v.set_labels:
            for text in v.set_labels:
                if text:
                    text.set_fontsize(16)
                    text.set_fontweight('bold')
        
        # subset_labels order for venn2: (left_only, right_only, both)
        terms = [left_only, right_only, both]
        
        if v.subset_labels:
            for i, (text_obj, term) in enumerate(zip(v.subset_labels, terms)):
                if text_obj and term:
                    items = [t.strip() for t in term.replace('\n', ',').split(',') if t.strip()]
                    if items:
                        formatted_text = '\n'.join(items[:7])
                        if len(items) > 7:
                            formatted_text += f'\n+{len(items)-7} more'
                        text_obj.set_text(formatted_text)
                        text_obj.set_fontsize(10)
                        text_obj.set_fontstyle('italic')
                    else:
                        text_obj.set_text('')
                elif text_obj:
                    text_obj.set_text('')
        
        plt.title("Venn Diagram (2 Circles)", fontsize=18, fontweight='bold', pad=20)
        
        output_path = Path(tempfile.mktemp(suffix=f".{export_format}"))
        
        if export_format == "png":
            plt.savefig(output_path, format='png', dpi=dpi, bbox_inches='tight', facecolor='white')
        else:
            plt.savefig(output_path, format='svg', bbox_inches='tight', facecolor='white')
        
        plt.close(fig)
        return output_path
    
    def _create_3_circle(self, left_label, middle_label, right_label,
                        left_only, middle_only, right_only,
                        left_middle, left_right, middle_right, all_three,
                        export_format, dpi):
        """Create a 3-circle Venn diagram"""
        left_label = left_label or "Set A"
        middle_label = middle_label or "Set B"
        right_label = right_label or "Set C"
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        v = venn3(
            subsets=(1, 1, 1, 1, 1, 1, 1),
            set_labels=(left_label, middle_label, right_label),
            ax=ax
        )
        
        colors = ['#ff9999', '#99ccff', '#99ff99', '#ffcccc', '#ccddff', '#ccffcc', '#ffffcc']
        
        if v.patches:
            for i, patch in enumerate(v.patches):
                if patch:
                    patch.set_alpha(0.4)
                    if i < len(colors):
                        patch.set_color(colors[i])
        
        if v.set_labels:
            for text in v.set_labels:
                if text:
                    text.set_fontsize(16)
                    text.set_fontweight('bold')
        
        terms = [left_only, middle_only, left_middle, right_only, left_right, middle_right, all_three]
        
        if v.subset_labels:
            for i, (text_obj, term) in enumerate(zip(v.subset_labels, terms)):
                if text_obj and term:
                    items = [t.strip() for t in term.replace('\n', ',').split(',') if t.strip()]
                    if items:
                        formatted_text = '\n'.join(items[:5])
                        if len(items) > 5:
                            formatted_text += f'\n+{len(items)-5} more'
                        text_obj.set_text(formatted_text)
                        text_obj.set_fontsize(9)
                        text_obj.set_fontstyle('italic')
                    else:
                        text_obj.set_text('')
                elif text_obj:
                    text_obj.set_text('')
        
        plt.title("Venn Diagram (3 Circles)", fontsize=18, fontweight='bold', pad=20)
        
        output_path = Path(tempfile.mktemp(suffix=f".{export_format}"))
        
        if export_format == "png":
            plt.savefig(output_path, format='png', dpi=dpi, bbox_inches='tight', facecolor='white')
        else:
            plt.savefig(output_path, format='svg', bbox_inches='tight', facecolor='white')
        
        plt.close(fig)
        return output_path