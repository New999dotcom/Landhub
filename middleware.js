const r=require("express");
const app=r();
app.use(r.json());
app.use((req, res, next) => {
    console.log('middleware executed', req.originalUrl);
    next();
});
app.get('/home', (req, res) => {
    console.log('yes working');
    
    res.send('Hello World!');
});
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
app.post('/signup', (req, res) => {
    console.log('Data received:', req.body);
    res.send('Data received for signup');
});
