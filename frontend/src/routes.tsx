import { Navigate, useRoutes } from 'react-router-dom';
import Layout from './layout/Layout';
import Search from "./views/dss-system/steps/search/Search.tsx";

export default function RouterUrl() {
    return useRoutes([
        {
            path: '/',
            element: <Layout />,
            children: [
                { path: 'search', element: <Search /> },
                { path: '', element: <Navigate to={'/search'} /> },
                { path: '*', element: <Navigate to={'/search'} /> },
            ],
        },
    ]);
}
