const express=require("express");
const app=express();
const path=require("path");
app.use(express.urlencoded({ extended: true }));
app.use((req, res, next) => {
    console.log('middleware executed', req.originalUrl);    
    next();
});
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'css')));
app.get('/', (req, res) => {
    res.render('index', { title: 'Home Page' });
});
const data={
    name: "John Doejj",
    age: 30,
    city: "New york"    
}
app.get('/about', (req, res) => {
    res.render('about', { title: 'About Page',  });
});
app.get('/profile', (req, res) => {
    res.render('profile', { title: 'Profile Page', data: data });
});

app.get('/login', (req, res) => {
    res.render('login', { title: 'Login Page' });

});

app.post('/login', (req, res) => {
    const { name, age } = req.body;
    console.log(req.body);

    if (!name || !age) {
        return res.status(400).send('Name and age are required');
    }
    
    console.log(`Username: ${name}, Age: ${age}`);
    
    res.send(`Username: ${name}, age: ${age} is submitted`);    

})

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});