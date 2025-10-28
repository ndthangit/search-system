import { Box } from "@mui/material";
import { ToastContainer } from "react-toastify";
import Content from "./Content.tsx";
import Menu from "./Menu.tsx"

export default function Layout() {
    return (
        <Box sx={{ display: "flex", height: "100vh" }}>
            <Menu />
            <Content />
            <ToastContainer
                position="top-center"
                autoClose={3000}
                theme="light"
                style={{
                    width: "max-content",
                    minWidth: "220px",
                    maxWidth: "90%",
                }}
                pauseOnHover
            />
        </Box>
    );
}
