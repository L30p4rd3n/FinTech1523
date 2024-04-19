async function updatePassword(url){
	let old_password = document.getElementById('old_password').value;
	let new_password = document.getElementById('new_password').value;
	let what = {"old": old_password,
				"new": new_password};
	let response = await fetch(url, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json; charset=utf-8'
		},
		body: JSON.stringify(what)
	});
	let result = await response.json();
	window.location.href='/';
}

async function log_in(url){
	let login = document.getElementById("login").value;
	let passwd = document.getElementById("password").value;
	let what = {"login": login,
				"password": passwd,
				"remember": 1};
	let response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=utf-8'
		},
		body: JSON.stringify(what)
	});
	if(response.status === 401){
		console.log("adasdas"); // код для добавления одной ошибки.
	}else{
		let result = await response.json();
		window.location.href='/';
	}
	
}

async function deleteUser(url){
	let what = {"request": "DELETE"}; // actually, could be used in a single func, but 0xplt_ too lazy to implement, cuz backend dev
	let response = await fetch(url, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json; charset=utf-8'
		},
		body: JSON.stringify(what)
	});
	let result = await response.json();
	window.location.href='/';
}