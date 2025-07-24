const { name } = require("ejs");
const express = require("express");
const app = express();
const path = require("path");
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));

const t={
    name: "John Doejj",
    age: 30,
    city: "New york",
    car:"BMW",
    Cash: 1000
}
app.get('/signin', (req, res) => {
    res.render('signin', { title: 'Login Page' });
});

app.post('/signin', (req, res) => {
    const { name, age,city,car,cash } = req.body;
    console.log(req.body);
    if (!name || !age || !city || !car || !cash) {
        return res.status(400).send('All fields are required');
    }})

   app.listen(3000, () => {
    console.log('Server is running on port 3000');  }) 
