import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#8b5cf6", dark: "#6d28d9" },
    secondary: { main: "#00ffff" },
    background: {
      default: "#1a1b26",
      paper: "#232436",
    },
    text: {
      primary: "#e0e0ff",
      secondary: "#a3a3c2",
    },
  },
  typography: {
    fontFamily: `"JetBrains Mono", "Fira Code", monospace`,
    h4: {
      fontWeight: 700,
      letterSpacing: "0.5px",
      color: "#c4b5fd",
    },
    body1: {
      color: "#d6d6f5",
      fontSize: "0.95rem",
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          backgroundColor: "rgba(35, 36, 54, 0.85)",
          backdropFilter: "blur(10px)",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: "none",
          fontWeight: 600,
          fontFamily: `"JetBrains Mono", monospace`,
          "&:hover": {
            boxShadow: "0 0 16px rgba(139, 92, 246, 0.5)",
          },
        },
      },
    },
  },
});
