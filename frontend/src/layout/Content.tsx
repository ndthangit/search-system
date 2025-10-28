import {CircularProgress, Container} from '@mui/material';
import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';

export default function Content() {
    return (
        <Container>
            <Suspense fallback={<CircularProgress sx={{ fontSize: '110px', mt: '30vh' }} />}>
                <Outlet />
            </Suspense>
        </Container>
    );
}
