import { createTheme, type PaletteMode } from "@mui/material/styles";

export const getTheme = (mode: PaletteMode) =>
  createTheme({
    palette: {
      mode,
      ...(mode === "light"
        ? {
            // Light mode
            primary: { main: "#2563eb", dark: "#1d4ed8" },
            secondary: { main: "#64748b" },
            background: {
              default: "#ffffff",
              paper: "#ffffff",
            },
            text: {
              primary: "#1a1a1a",
              secondary: "#6b7280",
            },
          }
        : {
            // Dark mode
            primary: { main: "#3b82f6", dark: "#2563eb" },
            secondary: { main: "#94a3b8" },
            background: {
              default: "#0f172a",
              paper: "#1e293b",
            },
            text: {
              primary: "#f1f5f9",
              secondary: "#94a3b8",
            },
          }),
    },
    typography: {
      fontFamily: `"Inter", "Roboto", "Helvetica", "Arial", sans-serif`,
      h3: {
        fontWeight: 700,
      },
      h6: {
        fontWeight: 700,
      },
      body1: {
        fontSize: "1rem",
      },
      body2: {
        fontSize: "0.875rem",
      },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: "none",
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 8,
            textTransform: "none",
            fontWeight: 600,
          },
          contained: {
            boxShadow: "none",
            "&:hover": {
              boxShadow: "none",
            },
          },
        },
      },
    },
  });

// Default theme for backward compatibility
export const theme = getTheme("light");
