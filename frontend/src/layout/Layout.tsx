import { Box, CssBaseline } from "@mui/material";
import { ToastContainer } from "react-toastify";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Outlet } from "react-router-dom";
import { ThemeProvider } from "../themes/ThemeContext";

const queryClient = new QueryClient();

export default function Layout() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <CssBaseline />

        <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
          <Outlet />
          <ToastContainer
            position="top-center"
            autoClose={3000}
            theme="colored"
            style={{
              width: "max-content",
              minWidth: "220px",
              maxWidth: "90%",
            }}
            pauseOnHover
          />
        </Box>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
