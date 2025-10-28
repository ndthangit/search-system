import { Navigate, useRoutes } from 'react-router-dom';
import Layout from './layout/Layout';
import Search from "./views/search/Search.tsx";
import Import from "./views/import/Import.tsx";

export default function RouterUrl() {
    return useRoutes([
        {
            path: '/',
            element: <Layout />,
            children: [
                { path: 'search', element: <Search /> },
                { path: 'import', element: <Import /> },
                { path: '', element: <Navigate to={'/search'} /> },
            ],
        },
    ]);
}
