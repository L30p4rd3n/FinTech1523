async function log_in(url){
	
	let login = document.getElementById("login").value;
	let password = document.getElementById("password").value;
	let what = {"login": login,
				"new": password};
	let response = await fetch(url, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json; charset=utf-8'
		},
		body: JSON.stringify(what)
	});
	let result = await response.json();
	if(result.response == 204){
		// здесь должен быть код для окна вида "пользователь не существует"
	}else if(result.response == 304){
		// здесь должен быть код для окна вида "неправильный пароль"
	}else{
		window.location.href="/";
	}
}