document.addEventListener('DOMContentLoaded', () => {
  let CurrentDateElement = document.getElementById('CurrentDate');
  let Options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  CurrentDateElement.textContent = new Date().toLocaleDateString('en-IN', Options);

  const MenuData = [
    { Id: 1, Name: "Aloo Paratha With Curd", Meal: "Breakfast", Rating: 4.5, Calories: 450, Recommended: true },
    { Id: 2, Name: "Oily Chole Bhature", Meal: "Lunch", Rating: 2.1, Calories: 800, Recommended: false },
    { Id: 3, Name: "Dal Makhani & Rice", Meal: "Dinner", Rating: 4.8, Calories: 550, Recommended: true },
    { Id: 4, Name: "Overcooked Cabbage", Meal: "Lunch", Rating: 1.5, Calories: 120, Recommended: false }
  ];

  let MenuContainer = document.getElementById('MenuContainer');

  function RenderMenu() {
    MenuContainer.innerHTML = '';
    MenuData.forEach(Item => {
      let ItemDiv = document.createElement('div');
      ItemDiv.className = 'Menu_Item';
      
      let BadgeClass = Item.Recommended ? 'Badge_Eat' : 'Badge_Skip';
      let BadgeText = Item.Recommended ? 'Smart Suggestion: Eat' : 'Smart Suggestion: Skip';

      let SvgStar = `<svg class="Star_Icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`;

      ItemDiv.innerHTML = `
        <div class="Item_Info">
          <h3>${Item.Name} <span class="Suggestion_Badge ${BadgeClass}">${BadgeText}</span></h3>
          <p>${Item.Meal} | Calories: ${Item.Calories}</p>
        </div>
        <div class="Item_Actions">
          <div class="Rating" data-id="${Item.Id}">
            ${SvgStar.replace('class="Star_Icon"', 'class="Star_Icon" data-value="1"')}
            ${SvgStar.replace('class="Star_Icon"', 'class="Star_Icon" data-value="2"')}
            ${SvgStar.replace('class="Star_Icon"', 'class="Star_Icon" data-value="3"')}
            ${SvgStar.replace('class="Star_Icon"', 'class="Star_Icon" data-value="4"')}
            ${SvgStar.replace('class="Star_Icon"', 'class="Star_Icon" data-value="5"')}
          </div>
        </div>
      `;
      MenuContainer.appendChild(ItemDiv);
    });

    AttachRatingListeners();
  }

  function AttachRatingListeners() {
    let Ratings = document.querySelectorAll('.Rating');
    Ratings.forEach(RatingContainer => {
      let Stars = RatingContainer.querySelectorAll('.Star_Icon');
      Stars.forEach(Star => {
        Star.addEventListener('click', (Event) => {
          let Value = parseInt(Event.currentTarget.getAttribute('data-value'));
          UpdateStars(RatingContainer, Value);
        });
      });
    });
  }

  function UpdateStars(Container, Value) {
    let Stars = Container.querySelectorAll('.Star_Icon');
    Stars.forEach(Star => {
      let StarValue = parseInt(Star.getAttribute('data-value'));
      if (StarValue <= Value) {
        Star.classList.add('Active');
      } else {
        Star.classList.remove('Active');
      }
    });
  }

  let SuggestionForm = document.getElementById('SuggestionForm');
  SuggestionForm.addEventListener('submit', (Event) => {
    Event.preventDefault();
    let Text = document.getElementById('SuggestionText').value;
    if(Text.trim() !== '') {
      alert('Transmission Successful!');
      SuggestionForm.reset();
    }
  });

  RenderMenu();
});
