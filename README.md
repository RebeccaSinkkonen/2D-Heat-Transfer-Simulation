# 2D-Heat-Transfer-Simulation
 Introduction
This project presents a 2D heat transfer simulation using a numerical energy-balance approach. The goal is to simulate heat diffusion across a rectangular plate divided into a grid of cells, where each cell exchanges heat with its neighbors. The user can control initial and boundary conditions, select a point for monitoring, generate graphs, save and load states, and produce a full report.
MainWindow (Opening Menu)
Includes four main buttons: Start Simulation, Show Video, Open Document, About. This menu serves as the gateway for launching the simulation.
SimulationWindow (Main Simulation Window)
This is the core of the software, where the simulation is visually executed. It includes the user interface, parameter control, heatmap display, and graphs. It manages user input, visual rendering, and animation. Input fields are available for temperature, mass, and specific heat values. Users can customize the colormap by selecting minimum, middle, and maximum temperature colors. QTimer is used to advance the simulation in regular time intervals.
To optimize performance, the visual display is updated every two steps instead of each time step. This improves speed without compromising output quality. My enhancement to the program was the addition of hot and cold spots: the user can place exactly one hot spot and one cold spot before the simulation begins (t = 0), which clamp the temperature of those cells to the specified hot or cold values.
Summary of Functions
    • __init__: Initializes window, state, and tracking lists
    • init_ui: Builds the user interface
    • init_timer: Sets up QTimer for regular updates
    • toggle_simulation: Starts/stops the simulation, connects CalculationWindow
    • timer_method: Performs regular time steps, calls 
CalculationWindow.calculations()
    • calculate_point_dt: Computes temperature derivative at selected point
    • on_click: Selects a point on the heatmap
    • select_color, build_colormap, update_colormap: Customize and update color gradient
    • open_graph: Opens graph window
    • save_simulation_state, load_simulation_state: Save/load .pkl simulation state
    • export_to_csv, export_pdf_report: Export results to CSV or PDF
    • clear_colormap: Clears current visual map
    • enable_hot_spot_mode: Place exactly one hot spot before the simulation begins (t = 0)
    • enable_cold_spot_mode: Place exactly one cold spot before the simulation begins (t = 0)

Button Functions:
    • Start – Start the simulation
    • Clear – Reset the selected point
    • Open Graph – Show the graph of temperature and its derivative over time
    • Apply Colors – Apply a custom colormap
    • Save State – Save simulation state to a .pkl file
    • Load State – Load a previously saved .pkl file
    • Export to Excel – Export selected point data to a CSV file
    • Export to PDF – Create a PDF report with settings, colormap, and graphs
    • Keep Point – Preserve the selected point even after restarting or clearing the simulation
    • Add Hot Spot – Place exactly one hot spot before the simulation begins (t = 0)
    • Add Cold Spot – Place exactly one cold spot before the simulation begins (t = 0)

GraphWindow (Graph Display Window)
Opens when the user chooses to plot a graph for a selected point. Displays temperature and derivative (dT/dt) graphs over time. Allows saving the graphs as image files and exporting the data to a CSV file for further analysis.
Summary of Functions
    • __init__, initUI: Setup graph interface
    • draw_graph: Display temperature/dT graphs
    • clear_graph: Clears graph area
    • export_to_csv: Saves data to CSV
    • save_graph: Saves image of the graph


Calculations.py (Computation Logic)
This file handles the core 2D heat transfer calculations using a basic energy-balance method. It updates each cell’s temperature based on its neighbors and the specified physical parameters.
The CalculationWindow class forms the physical core of the simulation. It receives all inputs from the main simulation window (initial temperature, boundary conditions, mass, specific heat) and uses them to compute temperature evolution over time.
At each time step, the temperature of interior cells is updated based on the difference between a cell and its four neighbors (up, down, left, right). Special updates are performed for corner and edge-center points using geometrically adapted neighbors. For these special points, heat rate is also computed and temporarily stored.
After each update, boundary conditions are re-applied to all edges, including averaging at corners for stability and accuracy. Additionally, any user-placed hot or cold spots are enforced each timestep by clamping those cells to the specified hot or cold temperature.
Summary of  Functions
    • __init__: Sets initial temperature grid and physical parameters
    • apply_bc: Enforces boundary conditions
    • _neighbors: Returns appropriate neighbors for corner/edge points
    • calculations: Main heat transfer update per time step
    • enforce_hot_cold_spots: Clamp user-defined hot and cold spots to specified hot/cold temperatures each time step

How to Use the Software
When the program launches, the user is presented with the main control window. In this window, the user enters the initial temperature and boundary temperatures for each edge of the grid. The user also sets the cell’s mass and specific heat capacity (in kg and J/kg·°C), and selects a custom color gradient for the heatmap—defining colors for minimum, midpoint, and maximum temperatures. Clicking the "Apply Colors" button applies the selected palette. Before starting the simulation, the user may click any cell to monitor its temperature and temperature rate (derivative) over time.
Clicking "Start" begins the simulation. The heatmap is updated visually every two time steps for performance optimization. If the “Keep Point” checkbox is selected, the chosen point remains active even when the simulation is restarted with different boundary conditions or colors. This allows for consistent comparisons across different simulation scenarios.
Before starting the simulation, the user may:
Click any cell to monitor its temperature and temperature rate (derivative) over time.
Click Add Hot Spot or Add Cold Spot to place exactly one hot spot or cold spot on the plate—but only while the simulation time remains t = 0.

Clicking Start begins the simulation. The heatmap is updated visually every two time steps for performance optimization. If the “Keep Point” checkbox is selected, the chosen point remains active even when the simulation is restarted with different boundary conditions or colors. This allows for consistent comparisons across different simulation scenarios.

When the simulation ends, users can:
    • Save the current simulation state to a .pkl file
    • Export the selected point’s data to a CSV file
    • Generate a PDF report including the simulation settings, color map, and graphs
    • Load a previously saved state and export a PDF directly from it
If the loaded graphs do not match the saved data, a warning is shown and PDF generation is disabled.
Input Validation
This validation is embedded within the simulation window. The software checks user-entered values (temperatures, mass, specific heat) in real time to ensure they fall within physical bounds. If a value is unreasonable (e.g., negative or excessively high temperature), a warning is shown to prevent invalid simulation results or crashes.

Challenges and Learnings
One of the main challenges was understanding the time-stepping mechanism: how to determine the correct dt based on grid spacing and material properties, and how it ties into the QTimer that updates the GUI. Synchronizing the simulation steps with the visual update interval (every two steps) was essential to achieve smooth and realistic animation without compromising speed.
Another early difficulty was realizing how to partially replace loops with matrix and vector operations. While some loops are still used—for example, when handling special points like corners—the main updates for the inner grid cells are now done using vectorized NumPy operations. This significantly improved performance and simplified the update logic. It required a new way of thinking, especially in setting up matrix slicing and ensuring correct broadcasting behavior. 
Another difficulty was handling point selection and data tracking. The software allows the user to click on a cell to track its temperature and rate of change over time. Managing the state of this point—especially when restarting the simulation, loading different scenarios.
Additionally, implementing and updating special points—specifically corners and edge-midpoints—posed challenges. Each special point required a tailored neighbor selection and a custom heat update rule. Ensuring accurate and stable calculations for these non-standard geometries added complexity to the code structure and testing.

