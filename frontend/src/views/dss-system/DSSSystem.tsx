import { useState } from "react";
import {
    Box,
    Button,
} from "@mui/material";
import {steps} from "./const.ts";
import FormInput from "./steps/form/FormInput.tsx";


export default function Import() {
    const [activeStep, setActiveStep] = useState(0);
    const [formData, setFormData] = useState({
        fullName: '',
        email: '',
        address: '',
    });

    const handleNext = () => {
        if (activeStep < steps.length - 1) {
            setActiveStep((prevStep) => prevStep + 1);
        }
    };

    const handleBack = () => {
        setActiveStep((prevStep) => prevStep - 1);
    };

    const handleChange = (field: string, value: string) => {
        setFormData((prevData) => ({
            ...prevData,
            [field]: value,
        }));
    };

    const getStepContent = (step: number) => {
        switch (step) {
            case 0:
                return <FormInput data={formData} handleChange={handleChange} />;
            case 1:
                return <Step2 data={formData} handleChange={handleChange} />;
            case 2:
                return <Step3 data={formData} handleChange={handleChange} />;
            case 3:
                return <Step4 data={formData} handleChange={handleChange} />;
            default:
                return 'Unknown step';
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ width: '100%', mt: 4 }}>
                <Stepper activeStep={activeStep} alternativeLabel>
                    {steps.map((label) => (
                        <Step key={label}>
                            <StepLabel>{label}</StepLabel>
                        </Step>
                    ))}
                </Stepper>

                <Box sx={{ mt: 4 }}>
                    {getStepContent(activeStep)}

                    <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                        <Button
                            color="inherit"
                            disabled={activeStep === 0}
                            onClick={handleBack}
                            sx={{ mr: 1 }}
                        >
                            Back
                        </Button>
                        <Box sx={{ flex: '1 1 auto' }} />
                        <Button onClick={handleNext}>
                            {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
                        </Button>
                    </Box>
                </Box>
            </Box>
        </Container>
    );
}
