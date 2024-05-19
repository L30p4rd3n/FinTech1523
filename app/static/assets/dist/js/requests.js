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
  var loginButton = document.querySelector('.big-blue-button');
    var errorMessage = document.getElementById('errorMessage center');
    loginButton.addEventListener('click', function() {
        errorMessage.style.display = 'block';
        setTimeout(function() {
            errorMessage.style.opacity = '1';
        }, 100);
        setTimeout(function() {
            errorMessage.style.opacity = '0';
            setTimeout(function() {
                errorMessage.style.display = 'none';
            }, 500);
        }, 2000);
    });
	}else{
		window.location.href='/';
	}
	
}
async function register(url){
	let email = document.getElementById("email").value;
	let login = document.getElementById("login").value;
	let passwd = document.getElementById("password").value;
	let what = {"login": login,
				"email": email,
				"password": passwd};
	let response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=utf-8'
		},
		body: JSON.stringify(what)
	});
	if(response.status === 400){
	var loginButton = document.querySelector('.big-blue-button');
    var errorMessage = document.getElementById('errorMessage center');
    loginButton.addEventListener('click', function() {
        errorMessage.style.display = 'block';
        setTimeout(function() {
            errorMessage.style.opacity = '1';
        }, 100);
        setTimeout(function() {
            errorMessage.style.opacity = '0';
            setTimeout(function() {
                errorMessage.style.display = 'none';
            }, 500);
        }, 2000);
    });
	}
	if(response.ok){
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

var endpoint = "";
var money = 0, salary=0, day=1, opt=0;
var result = {};

async function getOptionURL(url){
	opt = document.getElementById("chooseOption").value;
	let response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'text/plain;charset=utf8'
		},
		body: opt
	});
	if(response.status == 200){
		endpoint = await response.text();
	}else if(response.status == 204){
		console.log("уже поработал");
	}else if (response.status == 202){
		log("Игра окончена. Спасибо за потраченное на нее время! Через 10 секунд вас автоматически переместит на главную страницу, где будут выведены советы по улучшению финансового профиля.");
		await sleep(10000);
		window.location.href='/'
	}
	else{
		console.log(response.status);
	}
}

async function showFields() {
    var d1 = document.getElementById('d1');
    var d2 = document.getElementById('d2');
	d1.placeholder = '';
	d2.placeholder = '';
	
    if (opt == 3 || opt == 4) {
		d1.style.display = '';
		d2.style.display = '';
		d1.placeholder = 'Номер акции';
		d2.placeholder = 'Количество';
    }else if (opt == 6) {
		d1.style.display = '';
		d2.style.display = '';
		d1.placeholder = '1-3 Камень-бумага';
		d2.placeholder = 'Ставка';
    }else if (opt == 7) {
		d1.style.display = 'block';
		d2.style.display = 'none';
		d1.placeholder = 'Ставка';
		d2.style.placeholder = '';
    }
	else {
		d1.style.display = 'none';
		d2.style.display = 'none';
		d1.style.placeholder = '';
		d2.style.placeholder = '';
    }
}

async function sendData(url){
	var response = "";
	if(opt == 3 || opt == 4 || opt == 6){
		var num = document.getElementById("d1").value;
		var count = document.getElementById("d2").value;
		let data = {
		"num": num,
		"count": count		
		};
		response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json;charset=utf8'
		},
		body: JSON.stringify(data)
	});
	}else if(opt == 7){
		var count = document.getElementById("d1").value;
		response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain;charset=utf8'
			},
			body: count
		});
	}
	else{
		response = await fetch(url, {
		method: 'POST',
		});
	}
	
	if(response.status == 200){
			udata();
			await sleep(100);
			if (opt == 1){
				result = await response.json();
				if (result.success == 1){
					udata();
				await sleep(20);
					log("Вы усердно поработали за сверхурочные; Вам решили повысить зарплату до " + result.salary);
				}else{
					udata();
				await sleep(20);
					log("Вы усердно поработали за сверхурочные");
				}
			}else if(opt == 2){
				result = await response.json();
				log("Ваши акции:");
				for(var i = 0; i < result.names.length; i++){
					log("Акции компании " + result.names[i] + " в количестве " + result.amounts[i] + " на цену " + result.prices[i]);
				}
			}else if(opt == 3){
				udata();
				await sleep(20);
				log("Вы купили акции компании с id " + num + " в количестве " + count);
				
			}else if(opt == 4){
				udata();
				await sleep(20);
				log("Вы продали акции компании с id " + num + " в количестве " + count);
				
			}else if(opt == 6 || opt == 7){
				result = await response.json();
				log("Ваше значение:" + result.player);
				log("Значение дилера:" + result.bot);
				if(result.playerwon){
					log("Вы победили и получили " + count);
				}else{
					log("Вы проиграли и потеряли " + count);
				}
			}
		
	}else if(response.status == 204){
		console.log(204);
	}else if(response.status == 202){
		log("Игра окончена. Спасибо за потраченное на нее время!\n Через 10 секунд вас автоматически переместит на главую\n страницу, где будут выведены советы.");
		await sleep(10000);
		window.location.href='/'
	}else{
		console.log(response.status)
	}
}
async function udata(){
			var url = '/api/g/u';
			await sleep(10);
			let response = await fetch(url, {method: "POST"});
			let result = await response.json();
			for(let i = 1; i <= 10; i++){
				document.getElementById(i).innerText=result.stocks[i-1];
			}
			salary=result.salary;
			day=result.day;
			money=result.money;
			let logElement = document.getElementById('log');
			logElement.innerHTML = '';
			log("Текущий баланс: " + money); log("Текущая зарплата: " + salary); log("Текущий день: " + day); 
	}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function log(message) {
        let logElement = document.getElementById('log');
        let listItem = document.createElement('li');
        listItem.textContent = message;
        logElement.appendChild(listItem);
        }
		
async function getadv(){
	let url = "/getadv";
	let response = await fetch(url, {method: 'POST'});
	let data = await response.json();
	if(data.msg.length == 0){
		document.getElementById("adviceContainer").innerHTML = '<p class = "lead">Ваши советы еще не готовы. Повторим через 5 секунд...</p>';
		await sleep(5000);
		window.location.href="/";
	}else{
		let where = document.getElementById('adviceContainer');
		where.innerHTML = '';
		await sleep(15);
		for(let i = 0; i < 5; i++){
			let what = document.createElement('p');
			what.style.cssText = `
				font-size: 18px;
				line-height: 1.5;
				color: #666;
			`;
			document.getElementById("feet").style.width = "99vw";
			what.textContent = data.msg[i];
			where.appendChild(what);
		}
	}
}