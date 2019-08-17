# SunFlower
Read this in other languages: [English](README.md), [Русский](README.ru.md)
> The best culinary site with which you will cook like a professional 

If you're stuck indoors on a snow day, it's an excellent excuse for getting busy in the kitchen. Save yourself a trip to the shops by baking your own bread, and stay warm with hot drinks, casseroles and soup.

See an API documentations:   
<https://app.swaggerhub.com/apis-docs/ligonberry73/Sunflower/1.0.2>

![](screenshots/header.jpg)

See development process in Trello
<https://trello.com/b/OFXxIOOw/sunflower>

## Installation
OS X & Linux & Windows:    
    1. ``` https://gitlab.com/sunflower-cookbook/sunflower.git```     
    2. In project root dir create file ```.env```     
    3. In the file ```.env``` initialize environment variables ```USERNAME, DBNAME, SECRET_KEY```    
    4. Run ```docker-compose up```      
    Example .env file:       
```sh
    USERNAME=test_user
    DBNAME=test_db
    SECRET_KEY=r!idmujce0r-=p(fjl--2!xc#cl$#c1#9$=yupko05(e$q$v&7
```

Free ```Django Key Generator``` - https://www.miniwebtool.com/django-secret-key-generator/

## Usage example

If you want to commit and generate new swagger specification, you should export environment variables  ```USERNAME```, ```DBNAME```, ```SECRET_KEY```.   
Then swagger specification will be create on each commit in file ```data.json```. You can change file name in ```generate_api_doc.py``` 


## Features

0. Register using the site: name, password, e-mail (optional)
0. Sign up with a google account
0. Register with twitter
0. Sign up with facebook
0. Register with VK.com
0. Log in
1. Find the recipe by name
1. Find recipes with specified ingredients.
1. Find recipes with the specified tag.
1. Find recipes from a specific author.
2. View recipe list
2. View a list of recipes, sorted by rating
2. View a list of recipes, sorted by date added
3. Create a recipe (available only to registered users)
3. View a specific recipe: its description, list of ingredients, steps of this recipe
3. Update recipe (available only to the author of the recipe and administrator)
3. Add a new tag to the recipe (available only for the author of the recipe and administrator)
3. Add a comment to the recipe (available only to the registered user)
3. Delete recipe (available only to the author of the recipe and administrator)
3. Detach the tag from the recipe (available only to the author of the recipe and administrator)
4. View Recipe Comment List
4. Sort the list of comments by date added
4. Sort the list of comments by rating
4. Update comment (available only for the author of the recipe)
4. Delete the comment (available only to the author of the recipe and administrator)
5. Create a cookbook (available only to registered users)
5. Update the cookbook (available only to the cookbook author)
5. Add your own or someone else's recipe to the cookbook (available only to the author of the cookbook)
5. Delete the cookbook (available only for the cookbook author)


## Team

This project is a part of culinary system (https://gitlab.com/sunflower-cookbook).     
Our development team:   
  
[![Shinkevich Gleb](https://gitlab.com/uploads/-/system/user/avatar/2651181/avatar.png?width=400)](https://gitlab.com/dubhad) | [![Molchanov Ivan](https://secure.gravatar.com/avatar/c7df9f5465e49b3e9c027e0ec27beeee?s=180&d=identicon)](https://github.com/kevva) | [![Darya Litvinchuk](https://gitlab.com/uploads/-/system/user/avatar/2707506/avatar.png?width=400)](https://gitlab.com/ligonberry)
---|---|---
[Shinkevich Gleb](https://gitlab.com/dubhad) | [Molchanov Ivan](https://github.com/kevva) | [Litvinchuk Darya](https://github.com/kevva) 


## Contributing

1. Fork it (<https://gitlab.com/sunflower-cookbook/sunflower.git/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

MIT © [Darya Litvinchuk](https://www.linkedin.com/in/darya-litvinchuk-42aba6171/)
