import { Navigate, useRoutes } from 'react-router-dom';
import Layout from './layout/Layout';
import Search from "./views/dss-system/steps/search/Search.tsx";
import Import from "./views/dss-system/steps/form/FormInput.tsx";

export default function RouterUrl() {
    return useRoutes([
        {
            path: '/',
            element: <Layout />,
            children: [
                { path: 'search', element: <Search /> },
                { path: 'form', element: <Import /> },
                { path: '', element: <Navigate to={'/search'} /> },
            ],
        },
    ]);
}
