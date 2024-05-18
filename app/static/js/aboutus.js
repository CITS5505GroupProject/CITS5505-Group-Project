function copyEmail() {
    const email = 'support@survey.com';
    navigator.clipboard.writeText(email).then(() => {
        alert('Email successfully copied');
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}
