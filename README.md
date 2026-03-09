# 2D Heat Transfer Simulation

## Introduction
This project presents a 2D heat transfer simulation using a numerical energy-balance approach. The goal is to simulate heat diffusion across a rectangular plate divided into a grid of cells, where each cell exchanges heat with its neighbors. The user can control initial and boundary conditions, select a point for monitoring, generate graphs, save and load states, and produce a full report.

## SimulationWindow (Main Simulation Window)
This is the core of the software, where the simulation is visually executed. It manages user input, visual rendering, and animation.
* **Inputs:** Fields are available for temperature, mass, and specific heat values.
* **Customization:** Users can customize the colormap by selecting minimum, middle, and maximum temperature colors.
* **Performance:** A QTimer is used to advance the simulation. The visual display is updated every two steps instead of each time step to improve speed without compromising quality.
* **Enhancements:** Users can place exactly one hot spot and one cold spot before the simulation begins (at t = 0), which clamp the temperature of those cells.

## Summary of Functions
* **__init__**: Initializes window, state, and tracking lists.
* **init_ui**: Builds the user interface.
* **init_timer**: Sets up QTimer for regular updates.
* **toggle_simulation**: Starts/stops the simulation and connects the CalculationWindow.
* **timer_method**: Performs regular time steps and calls the calculation logic.
* **calculate_point_dt**: Computes temperature derivative at a selected point.
* **save_simulation_state / load_simulation_state**: Save or load .pkl simulation states.
* **export_pdf_report**: Exports results to a full PDF report.

## Calculations.py (Computation Logic)
This file handles the core 2D heat transfer calculations using a basic energy-balance method. It updates each cell’s temperature based on its neighbors and the specified physical parameters.



* **Numerical Approach:** Interior cells are updated based on the four neighbors: up, down, left, right.
* **Special Geometries:** Corner and edge-center points use geometrically adapted neighbors; heat rate (q̇) is also computed for these points.
* **Stability:** Boundary conditions are re-applied at each step, including averaging at corners for numerical stability.

## How to Use the Software
1. **Setup:** Enter initial and boundary temperatures, mass, and specific heat capacity.
2. **Point Monitoring:** Click any cell on the heatmap to track its temperature and derivative over time.
3. **Thermal Sources:** Use "Add Hot Spot" or "Add Cold Spot" to place sources before starting (at t = 0).
4. **Execution:** Click "Start" to begin the simulation.
5. **Keep Point:** Enable the “Keep Point” checkbox to preserve your monitored point across different simulation runs.

## Input Validation
Validation is embedded within the simulation window. The software checks user-entered values in real time to ensure they fall within physical bounds. If a value is unreasonable (e.g., negative mass), a warning is shown to prevent invalid results or crashes.

## Challenges and Learnings
* **Time-Stepping:** Determining the correct dt based on grid spacing and material properties was a major challenge for the time-stepping mechanism.
* **Vectorization:** Transitioning from loops to vectorized NumPy operations significantly improved performance and simplified the update logic.
* **Special Points:** Implementing custom neighbor rules for corners and edge-midpoints was complex but necessary for accurate calculations.
