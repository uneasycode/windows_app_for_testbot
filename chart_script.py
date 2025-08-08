import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Create a more organized flow diagram
fig = go.Figure()

# Define components with better positioning and proper shapes
components = [
    # Start point
    {"name": "Windows .exe", "x": 3, "y": 9, "width": 0.8, "height": 0.6, "color": "#8A2BE2", "shape": "diamond"},
    
    # Main GUI
    {"name": "Desktop GUI", "x": 3, "y": 7.5, "width": 1.2, "height": 0.8, "color": "#1FB8CD", "shape": "rect"},
    
    # GUI Tabs (arranged horizontally)
    {"name": "Bot Control", "x": 1, "y": 6, "width": 0.8, "height": 0.5, "color": "#1FB8CD", "shape": "rect"},
    {"name": "Response Mgmt", "x": 2, "y": 6, "width": 0.8, "height": 0.5, "color": "#1FB8CD", "shape": "rect"},
    {"name": "Media Files", "x": 3, "y": 6, "width": 0.8, "height": 0.5, "color": "#1FB8CD", "shape": "rect"},
    {"name": "Live Messages", "x": 4, "y": 6, "width": 0.8, "height": 0.5, "color": "#1FB8CD", "shape": "rect"},
    {"name": "Settings", "x": 5, "y": 6, "width": 0.8, "height": 0.5, "color": "#1FB8CD", "shape": "rect"},
    
    # Background processes
    {"name": "Bot Thread", "x": 1, "y": 4, "width": 1, "height": 0.6, "color": "#2E8B57", "shape": "rect"},
    {"name": "Monitor Thread", "x": 4, "y": 4, "width": 1, "height": 0.6, "color": "#2E8B57", "shape": "rect"},
    {"name": "System Tray", "x": 5.5, "y": 7.5, "width": 0.8, "height": 0.6, "color": "#5D878F", "shape": "rect"},
    
    # File operations
    {"name": "responses.json", "x": 2, "y": 2, "width": 1, "height": 0.6, "color": "#D2BA4C", "shape": "rect"},
    {"name": "Media Storage", "x": 3.5, "y": 2, "width": 1, "height": 0.6, "color": "#D2BA4C", "shape": "rect"},
    {"name": "Config (.env)", "x": 5, "y": 2, "width": 1, "height": 0.6, "color": "#D2BA4C", "shape": "rect"},
    
    # External API
    {"name": "Telegram API", "x": 1, "y": 0.5, "width": 1.2, "height": 0.6, "color": "#1FB8CD", "shape": "rect"}
]

# Draw rectangles and diamonds for components
for comp in components:
    if comp["shape"] == "rect":
        # Draw rectangle
        fig.add_shape(
            type="rect",
            x0=comp["x"] - comp["width"]/2, y0=comp["y"] - comp["height"]/2,
            x1=comp["x"] + comp["width"]/2, y1=comp["y"] + comp["height"]/2,
            fillcolor=comp["color"],
            line=dict(color="black", width=2)
        )
    elif comp["shape"] == "diamond":
        # Draw diamond using path
        fig.add_shape(
            type="path",
            path=f"M {comp['x']} {comp['y'] + comp['height']/2} " +
                 f"L {comp['x'] + comp['width']/2} {comp['y']} " +
                 f"L {comp['x']} {comp['y'] - comp['height']/2} " +
                 f"L {comp['x'] - comp['width']/2} {comp['y']} Z",
            fillcolor=comp["color"],
            line=dict(color="black", width=2)
        )
    
    # Add text labels
    fig.add_annotation(
        x=comp["x"], y=comp["y"],
        text=comp["name"],
        showarrow=False,
        font=dict(size=12, color="white"),
        xanchor="center",
        yanchor="middle"
    )

# Add flow arrows
arrows = [
    # Main flow
    (3, 8.4, 3, 8.1),      # exe to GUI
    (3, 7.1, 3, 6.5),      # GUI to tabs
    (3, 7.5, 5.1, 7.5),    # GUI to System Tray
    
    # Tab to process connections
    (1, 5.7, 1, 4.6),      # Bot Control to Bot Thread
    (2, 5.7, 2, 2.6),      # Response Mgmt to responses.json
    (3, 5.7, 3.5, 2.6),    # Media Files to Media Storage
    (4, 5.7, 4, 4.6),      # Live Messages to Monitor Thread
    (5, 5.7, 5, 2.6),      # Settings to Config
    
    # Background process flows
    (1, 3.4, 1, 1.1),      # Bot Thread to Telegram API
    (4, 3.4, 3.5, 7),      # Monitor Thread back to GUI
    (1.5, 2, 2.5, 3.7),    # responses.json to Monitor Thread
]

for x1, y1, x2, y2 in arrows:
    fig.add_annotation(
        x=x2, y=y2,
        ax=x1, ay=y1,
        xref="x", yref="y",
        axref="x", ayref="y",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="black",
        showarrow=True
    )

# Add legend
legend_items = [
    {"name": "GUI Components", "color": "#1FB8CD"},
    {"name": "Bot Processes", "color": "#2E8B57"},
    {"name": "File Operations", "color": "#D2BA4C"},
    {"name": "System Integration", "color": "#5D878F"}
]

for i, item in enumerate(legend_items):
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color=item["color"], symbol="square"),
        name=item["name"],
        showlegend=True
    ))

# Update layout
fig.update_layout(
    title="Windows App Flow Diagram",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 6.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 10]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h', 
        yanchor='bottom', 
        y=1.02, 
        xanchor='center', 
        x=0.5
    )
)

# Save the chart
fig.write_image("windows_app_flow.png")