const r=require("express");
const app=r();
app.use((req, res, next) => {
    console.log('middleware executed', req.originalUrl);

    next();
});

app.get('/home', (req, res) => {
    res.send('Hello World!');
}   );

app.get('/e', (req, res) => {
    res.send('Hello second!');
}   );

app.get('/me', (req, res) => {
    res.send('Hello third!');
}   );

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});

const d={
    name: "John Doe",
    age: 30
};  

for (let i=0; i<d.name.length; i++) {
    console.log(d.name[i]);
}

app.post('/signup', (req, res) => {
    console.log('Data received:', req.body);
    res.send('Data received for signup');
});

