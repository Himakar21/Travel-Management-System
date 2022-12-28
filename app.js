require('dotenv').config();
let mysql = require('mysql');
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const e = require('express');
const { connect } = require('http2');
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static("public"));

let connection = mysql.createConnection(
  {
      host:"localhost",
      user:"root",
      password:"793164",
      multipleStatements: true
  }
);

connection.connect(function(err){
    if(err)
    {
        throw err;
    }
    console.log(' ** Connected to MySQL Database **');
    connection.query("create database if not exists traveldbms;");
    connection.query("use traveldbms;");
});



app.get('/create/:adminId',async function(req,res){
    if (req.params['adminId'] === process.env.ADMIN_ID)
    {
      const fs = require('fs');
      var queries = fs.readFileSync('./tableDefinition.sql',{encode:'utf-8',flag:'r'}).toString();
      queries = queries.replace( /[\n\r]+/gm, "" );
      await connection.query(queries,function(err,result){
          if(err)
          {
             res.send(`<p>${err}</p>`);
          }
          else
          {
            res.send("tables created successfully...");
          }
      });
    }
});

//app.get('/',function(req,res){
//  res.render('Home.ejs',{type:"home"});
//});

// app.get('/signup',function(req,res){
//   res.render('tableInfoForm.ejs');
// });

app.get('/',function(req,res){
  connection.query("select * from flights",function(err,result){
    if (err)
    {
      res.send(`<p>${err}</p>`);
    }
    else
    {
      if (result.length == 0)
      {
          result = [{"fnumber" : 1,"flight name":2,"source":5,"destination":6,"price":7}];
          res.render("displayFlightTable.ejs",{table:"empty",result:result});
      }
      else
      {
        console.log();
        res.render("displayFlightTable.ejs",{table:"not empty",result:result});
      }
    }
  });
});


app.get('/query',function(req,res){   
  res.render("querybox.ejs",{display:"No",result:[{}]});
})

app.post('/query',function(req,res){
    if (req.body.sqlQuery != '')
    {
      var q1 =req.body.sqlQuery;
      connection.query(req.body.sqlQuery,function(err,result){
        if(err)
        {
          res.send(`<p> ${err} </p>`)
        }
        else
        {
            if("affectedRows" in result)
            {
              res.render("querybox.ejs",{q:q1,display:"yes",result:[{}],affectedRows : result["affectedRows"]});
            }
            else
            {
              res.render("querybox.ejs",{q:q1,display:"yes",result:result});
            }
        }
      });
    }
    else
    {
      res.send('Empty query!!!');
    }
});

app.get('/addFlights',function(req,res){
  res.render("flightInfoForm.ejs");
});

app.post('/addFlights',function(req,res){
    data = req.body;
    connection.query(`insert into flights values("${data["fnumber"]}","${data["flightname"]}","${data["src"]}","${data["dest"]}",${data["price"]});`,function(err,result){
      if (err)
      {
        res.send(`<p>${err}</p>`);
      }
      else
      {
         res.redirect("/");
      }
    });
});

app.get("/updateUser/:id",function(req,res){
    var id = req.params.id;
    connection.query(`select * from flights where flight_number = "${id}"`,function(err,result){
        if(err)
        {
          res.send(`<p>${err}</p>`);
        }
        else
        {
          res.render("updateForm.ejs",{result:result[0]});
        }
    });
});

app.post("/updateUser/:id",function(req,res){
    connection.query(`update flights set flight_name = "${req.body.flightname}",src = "${req.body.src}",dest = "${req.body.dest}", fareperperson = ${req.body.price} where flight_number="${req.body.fnumber}";`,function(err,result){
      if (err)
      {
        res.send(`<p>${err}</p>`);
        //throw err;
      }
      else
      {
        console.log(result)
        res.redirect('/');
      }
    });
});

app.get("/deleteUser/:id",function(req,res){
    connection.query(`Delete from flights where flight_number = "${req.params.id}"`,function(err,result){
      if(err)
      {
        res.send(`<p>${err}</p>`);
      }
      else
      {
        res.redirect("/");
      }
    });
});

app.listen(3310,()=>{
  console.log('app running on port '+ 3310);
});
