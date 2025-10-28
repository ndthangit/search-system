import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import { ToastContainer } from "react-toastify";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Content from "./Content.tsx";
import Menu from "./Menu.tsx";
import { theme } from "../themes/theme.tsx";

const queryClient = new QueryClient();

export default function Layout() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />

        <Box sx={{ display: "flex", height: "100vh", bgcolor: "background.default" }}>
          <Menu />
          <Content />
          <ToastContainer
            position="top-center"
            autoClose={3000}
            theme="dark"
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
