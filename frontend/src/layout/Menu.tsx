import { NavLink } from "react-router-dom";
import {
    Drawer,
    List,
    ListItemButton,
    ListItemText,
    Toolbar,
    Typography,
} from "@mui/material";

const drawerWidth = 260;

type TMenu = {
    title: string;
    path: string;
};

const menu: TMenu[] = [
    { title: "Search", path: "/search" },
    { title: "Import", path: "/form" },
];

export default function Menu() {
    return (
        <Drawer
            variant="permanent"
            anchor="left"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                "& .MuiDrawer-paper": {
                    width: drawerWidth,
                    boxSizing: "border-box",
                    borderRight: "1px solid",
                    borderColor: "divider",
                    p: 2,
                },
            }}
        >
            <Toolbar>
                <Typography variant="h6" fontWeight={600}>
                    Logo
                </Typography>
            </Toolbar>

            <List>
                {menu.map((item) => (
                    <ListItemButton
                        key={item.path}
                        component={NavLink}
                        to={item.path}
                        sx={{
                            borderRadius: 100,
                            mb: 1,
                            "&.active": {
                                bgcolor: "action.selected",
                                "& .MuiListItemText-primary": { fontWeight: 600 },
                            },
                            "&:hover": {
                                bgcolor: "action.hover",
                            },
                        }}
                    >
                        <ListItemText primary={item.title} />
                    </ListItemButton>
                ))}
            </List>
        </Drawer>
    );
}
