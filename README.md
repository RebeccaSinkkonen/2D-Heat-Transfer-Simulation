# 2D Heat Transfer Simulation

## Introduction
This project presents a 2D heat transfer simulation using a numerical energy-balance approach. The goal is to simulate heat diffusion across a rectangular plate divided into a grid of cells, where each cell exchanges heat with its neighbors. The user can control initial and boundary conditions, select a point for monitoring, generate graphs, save and load states, and produce a full report.

## MainWindow (Opening Menu)
The Opening Menu serves as the gateway for launching the simulation. It includes four main buttons:
* **Start Simulation**
* **Show Video**
* **Open Document**
* **About** > **Note:** The "About" document has not been uploaded to this repository as it contains personal information and details regarding my personal space.

## SimulationWindow (Main Simulation Window)
This is the core of the software, where the simulation is visually executed. It manages user input, visual rendering, and animation. 

* **Input Fields:** Available for temperature, mass, and specific heat values. 
* **Customization:** Users can customize the colormap by selecting minimum, middle, and maximum temperature colors. 
* **Performance Optimization:** A QTimer is used to advance the simulation. To improve speed without compromising output quality, the visual display is updated every two steps instead of each time step.
* **Enhancement:** The user can place exactly one hot spot and one cold spot before the simulation begins (at t = 0), which clamp the temperature of those cells to specified values.

### Summary of SimulationWindow Functions
* **__init__**: Initializes window, state, and tracking lists.
* **init_ui**: Builds the user interface, input fields, and buttons.
* **init_timer**: Sets up QTimer for regular updates.
* **toggle_simulation**: Starts/stops the simulation and connects the CalculationWindow.
* **timer_method**: Performs regular time steps and updates the visual heatmap.
* **calculate_point_dt**: Computes temperature derivative at a selected point.
* **save_simulation_state / load_simulation_state**: Save or load the simulation state using .pkl files.
* **export_to_csv / export_pdf_report**: Export results to CSV or generate a full PDF report.

## Calculations.py (Computation Logic)
This file handles the physical core of the simulation using a basic energy-balance method. It updates each cell’s temperature based on its neighbors and specified physical parameters.



* **Numerical Approach:** Interior cells are updated based on the four neighbors (up, down, left, right).
* **Special Geometries:** Special updates are performed for corner and edge-center points using geometrically adapted neighbors.
* **Stability:** Boundary conditions are re-applied at each step, including averaging at corners for numerical stability and accuracy.

## How to Use the Software
1. **Initial Setup:** Enter initial temperature, boundary conditions, mass, and specific heat capacity.
2. **Thermal Sources:** Before starting (at t = 0), you may place exactly one Hot Spot or Cold Spot on the plate.
3. **Point Monitoring:** Click any cell on the heatmap to track its temperature and derivative over time.
4. **Simulation:** Click **Start** to begin. The heatmap updates visually every two steps to optimize performance.
5. **Post-Simulation:** Save your state to a .pkl file, export data to CSV, or generate a PDF report.

## Input Validation
Validation is embedded within the simulation window. The software checks user-entered values in real time to ensure they fall within physical bounds. If a value is unreasonable (e.g., negative mass or excessively high temperature), a warning is shown to prevent invalid results or crashes.

## Challenges and Learnings
* **Time-Stepping Mechanism:** Understanding how to determine the correct dt based on grid spacing and material properties was a primary challenge.
* **Vectorization:** Replacing loops with vectorized **NumPy** operations significantly improved performance and simplified the update logic. It required a new way of thinking regarding matrix slicing and broadcasting.
* **Edge Case Implementation:** Implementing and updating special points (corners and edge-midpoints) was complex, as each required a tailored neighbor selection and a custom heat update rule.
