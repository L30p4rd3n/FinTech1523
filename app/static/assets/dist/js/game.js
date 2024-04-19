let goal = 1000000;
              let currentCapital = 0;
              let salary = 20000;
              let taxRate = 0.15;
              let month = 1;
              let isGameOver = false;
              let risk = 0;
          
              function showStatus() {
            document.getElementById('status').innerText = `
              Месяц ${month}
              Текущий капитал: ${currentCapital} рублей
              Цель: ${goal} рублей
            `;
          }
          
              function skipTurn() {
                month += 1;
                earnSalary();
                payTax();
                log("Вы хорошо поспали");
                showStatus();
              }
          
              function log(message) {
            let logElement = document.getElementById('log');
            let listItem = document.createElement('li');
            listItem.textContent = message;
            logElement.appendChild(listItem);
          }
          
          function earnSalary() {
            currentCapital += salary;
            log(`Вы получили зарплату! ${salary / 1000} тысяч рублей`);
            showStatus();
          }
          
          function payTax() {
            let taxAmount = currentCapital * taxRate;
            currentCapital -= taxAmount;
            log(`Вы заплатили налог в размере ${taxAmount} рублей.`);
            showStatus();
          }
          
              function invest() {
                month += 1;
                let choice = prompt("Выберите тип инвистиции:\n1. Стабильная\n2. Рисковая");
          
                switch (choice) {
                  case '1':
                    let amountStable = parseInt(prompt("Введите сколько вы хотите инвестировать: "));
                    if (currentCapital >= amountStable) {
                      currentCapital -= amountStable;
                      let incomeStable = amountStable * 0.05; // Пример стабильного дохода
                      currentCapital += incomeStable;
                      log(`Вы инвестировали ${amountStable} рублей в стабильные ивестиции.`);
                      log(`Вы стабильно получили ${incomeStable} рублей`);
                      showStatus();
                    } else {
                      log("У вас недостаточно денег для инвестици.");
                    }
                    break;
                  case '2':
                    let amountRisky = parseInt(prompt("Введите сколько вы хотите инвестировать: "));
                    if (currentCapital >= amountRisky) {
                      currentCapital -= amountRisky;
                      let chance = Math.random(); // Генерация случайного шанса (от 0 до 1)
                      if (chance < 0.5) { // 50% шанс потерять инвестицию
                        let loss = amountRisky * 0.3; // Пример потери
                        currentCapital -= loss;
                        log(`Вы потеряли ${loss} рублей на рисковых инвестициях.`);
                      } else {
                        let incomeRisky = amountRisky * 0.2; // Пример дохода
                        currentCapital += incomeRisky;
                        log(`Вы инвестировали ${amountStable} рублей в рисковые ивестиции.`);
                        log(`Вы получили: ${incomeRisky} рублей`);
                      }
                      showStatus();
                    } else {
                      log("У вас недостаточно денег для инвестици.");
                    }
                    break;
                  default:
                    log("вы закончили");
                    break;
                }
                showStatus();
              }
          
              function playCasino() {
                month += 1;
          
                let itog = 0;
                let playAgain = true;
          
                while (playAgain) {
                  let choice = prompt("Выберите игру:\n1. Кости\n2. Автомат");
          
                  if (choice === '1') {
                    let bet = parseInt(prompt("Введите сколько вы хотите для игры в костях: "));
                    if (currentCapital >= bet) {
                      itog += diceGame(bet);
                    } else {
                      log("У вас недостаточно денег для игры.");
                    }
                  } else if (choice === '2') {
                    log("Вы играете на автоматах за 1000 рублей.");
                    itog += slotMachineGame();
                  } else {
                    log("Некоректный ввод.");
                  }
                  let playAgainInput = prompt("Вы хотатие сыграть еще раз? (да/нет): ");
                  playAgain = playAgainInput.toLowerCase() === 'да';
                  log(`Ваш выиграш: ${itog} рублей`);
                }
                showStatus();
          
                return itog;
              }
          
              function diceGame(betAmount) {
                let diceRoll = Math.floor(Math.random() * 6) + 1;
                let diceRollComp = Math.floor(Math.random() * 6) + 1;
          
                log(`Вы выбросили: ${diceRoll}`);
                log(`Диллер выбросил: ${diceRollComp}`);
          
                if (diceRoll > diceRollComp) {
                  log(`Поздравляю! Вы выйграли ${betAmount} рублей!`);
                  return betAmount;
                } else if (diceRoll < diceRollComp) {
                  log("Неповезло, вы проиграли.");
                  return -betAmount;
                } else {
                  log("Ничья.");
                  return 0;
                }
              }
          
              function slotMachineGame() {
                let betAmount = 1000;
                let symbols = ['♠', '♣', '♥', '♦'];
                let slot1 = symbols[Math.floor(Math.random() * symbols.length)];
                let slot2 = symbols[Math.floor(Math.random() * symbols.length)];
                let slot3 = symbols[Math.floor(Math.random() * symbols.length)];
          
                log(`На машине вот такие значки: ${slot1} ${slot2} ${slot3}`);
          
                if (slot1 === slot2 && slot2 === slot3) {
                  log(`Поздравляю! Вы выйграли ${betAmount * 10} рублей!`);
                  return betAmount * 10;
                } else {
                  log("Неповезло, вы проиграли.");
                  return -betAmount;
                }
              }
          
              // Связываем функцию invest() с кнопкой "Invest"
              document.getElementById('investButton').addEventListener('click', function() {
                invest();
              });
          
              // Запуск игры
              function startGame() {
                showStatus();
                earnSalary();
                payTax();
              }
          
              startGame();