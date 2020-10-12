var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get("/packets", function(req, res, next) {
    res.json([
        {src: '1.0.0.0', dst: '1.0.0.1'},
        {src: '2.0.0.0', dst: '2.0.0.1'}
    ]);
})

module.exports = router;
