import numpy as np

class CalculationWindow:
    """
    Simple 2D heat-transfer simulation using energy-balance updates.
    Uses mass, specific heat, and a conductance G = alpha * m * c to compute heat flow.
    """
    nx = 20 
    ny = 20 

    def __init__(self,
                 T_ic,      
                 T_top,    
                 T_bottom,  
                 T_left,    
                 T_right,  
                 mass,     
                 h_capacity):
        
        self.m_cell = mass
        self.cp     = h_capacity
        self.alpha  = 1.44e-7   

        self.T_top    = T_top
        self.T_bottom = T_bottom
        self.T_left   = T_left
        self.T_right  = T_right

        self.Lx, self.Ly = 100.0, 100.0
        self.nx, self.ny = CalculationWindow.nx, CalculationWindow.ny
        self.dx = self.Lx / (self.nx - 1)
        self.dy = self.Ly / (self.ny - 1)

        self.dt = (self.dx ** 2) / (4.0 * self.alpha) * 0.2 

        self.T = np.full((self.nx, self.ny), T_ic, dtype=float)
        
        self.current_hot_spots  = 0
        self.current_cold_spots = 0
        self.cold_spot_coords = []
        self.hot_spot_coords = []
        self.hot_temp = 200.0
        self.cold_temp = 0

        mid_col = (self.ny - 1) // 2
        mid_row = (self.nx - 1) // 2
        self.points = {
            'corner_top_left':     (0, 0),
            'corner_top_right':    (0, self.ny - 1),
            'corner_bottom_left':  (self.nx - 1, 0),
            'corner_bottom_right': (self.nx - 1, self.ny - 1),
            'middle_top':      (0, mid_col),
            'middle_bottom':   (self.nx - 1, mid_col),
            'middle_left':     (mid_row, 0),
            'middle_right':    (mid_row, self.ny - 1),}
        
        self.heat_rate    = {name: 0.0 for name in self.points}
        self.corner_heat_history = {name: [] for name in self.points if 'corner' in name}
        self.middle_heat_history = {name: [] for name in self.points if 'middle' in name}

        self.apply_bc()

    def apply_bc(self):
            """Apply Dirichlet BCs on edges, excluding corner points."""
            corner_points = {(0, 0), (0, self.ny - 1),
                            (self.nx - 1, 0), (self.nx - 1, self.ny - 1)}

            for j in range(self.ny):
                if (0, j) not in corner_points:
                    self.T[0, j] = self.T_bottom
                if (self.nx - 1, j) not in corner_points:
                    self.T[self.nx - 1, j] = self.T_top

            for i in range(self.nx):
                if (i, 0) not in corner_points:
                    self.T[i, 0] = self.T_left
                if (i, self.ny - 1) not in corner_points:
                    self.T[i, self.ny - 1] = self.T_right

            self.T[0, 0] = 0.5*(self.T_bottom + self.T_left)
            self.T[0, self.ny-1] = 0.5*(self.T_bottom + self.T_right)
            self.T[self.nx-1, 0] = 0.5*(self.T_top + self.T_left)
            self.T[self.nx-1, self.ny-1] = 0.5*(self.T_top + self.T_right)

    def _neighbors(self, name, i, j):
        """Return neighbor indices for a given special point key."""
    
        if name == 'middle_top':
            return [(1, j), (0, j - 1), (0, j + 1)]
        elif name == 'middle_bottom':
            return [(self.nx - 2, j), (self.nx - 1, j - 1), (self.nx - 1, j + 1)]
        elif name == 'middle_left':
            return [(i - 1, 0), (i + 1, 0), (i, 1)]
        elif name == 'middle_right':
            return [(i - 1, self.ny - 1), (i + 1, self.ny - 1), (i, self.ny - 2)]

        elif name == 'corner_top_left':
            return [(1, 0), (0, 1), (1, 1)]
        elif name == 'corner_top_right':
            return [(1, j),(0, j - 1),(1, j - 1)]
        elif name == 'corner_bottom_left':
            return [(i - 1, 0),(i, 1),(i - 1, 1)]
        elif name == 'corner_bottom_right':
            return [(i - 1, j),(i, j - 1),(i - 1, j - 1)]
        else:
             raise ValueError(f"Unknown point name: {name}")

    def calculations(self):
        """
        Perform one time step:
         - Uniform finite-difference update for all points
         - Still compute heat rates at special points
         - Re-apply BCs
        """
        w = self.T.copy()
        dt, m, cp = self.dt, self.m_cell, self.cp
        alpha = self.alpha
        dx2 = self.dx ** 2

        C = w[1:-1, 1:-1]
        R = w[1:-1, 2:  ] 
        L = w[1:-1, :-2]
        D = w[2:  , 1:-1] 
        U = w[:-2, 1:-1]

        dTsum = (R - C) + (L - C) + (D - C) + (U - C)
        self.T[1:-1, 1:-1] = C + (alpha * dt * dTsum) / dx2

        for name, (i, j) in self.points.items():
            T0 = w[i, j]
            neighbors = self._neighbors(name, i, j)

            q_dot = sum(alpha * m * cp * (w[ni, nj] - T0) for ni, nj in neighbors)
            self.heat_rate[name] = abs(q_dot)

            dTsum = sum(w[ni, nj] - T0 for ni, nj in neighbors)
            self.T[i, j] = T0 + (alpha * dt * dTsum) / dx2

        for name in self.points:
            qdot = self.heat_rate[name]
            if "corner" in name:
                self.corner_heat_history[name].append(qdot)
            elif "middle" in name:
                self.middle_heat_history[name].append(qdot)

        self.apply_bc()
        for i, j in self.cold_spot_coords:
            self.T[i, j] = self.cold_temp

        for i, j in self.hot_spot_coords:
            self.T[i, j] = self.hot_temp 

        return self.T

