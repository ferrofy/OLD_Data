const Search_Input = document.getElementById('Search_Input');
const Search_Btn = document.getElementById('Search_Btn');
const Image_Gallery = document.getElementById('Image_Gallery');
const Loader = document.getElementById('Loader');
const Error_Message = document.getElementById('Error_Message');
const Header = document.querySelector('.Header');
const Generating_Text = document.getElementById('Generating_Text');

const Generation_Steps = [
    "Initializing AI Engine...",
    "Analyzing Prompt...",
    "Rendering Base Image...",
    "Enhancing Details...",
    "Finalizing..."
];

let Search_Timeout = null;

const Fetch_Images = async (Query) => {
    if (!Query.trim()) return;

    Header.classList.add('Active');
    Image_Gallery.innerHTML = '';
    Error_Message.classList.add('Hidden');
    Loader.classList.remove('Hidden');

    let Step_Index = 0;
    Generating_Text.textContent = Generation_Steps[0];
    const Step_Interval = setInterval(() => {
        Step_Index++;
        if (Step_Index < Generation_Steps.length) {
            Generating_Text.textContent = Generation_Steps[Step_Index];
        }
    }, 800);

    try {
        const Api_Url = `https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(Query)}&gsrlimit=30&prop=pageimages&pithumbsize=800&format=json&origin=*`;

        const Response = await fetch(Api_Url);
        const Data = await Response.json();

        if (!Data.query || !Data.query.pages) {
            clearInterval(Step_Interval);
            Show_Error();
            return;
        }

        const Pages = Object.values(Data.query.pages);
        const Images = Pages.filter(Page => Page.thumbnail && Page.thumbnail.source);

        if (Images.length === 0) {
            clearInterval(Step_Interval);
            Show_Error();
            return;
        }

        setTimeout(() => {
            clearInterval(Step_Interval);
            Loader.classList.add('Hidden');
            Render_Images([Images[0]]);
        }, 4000);

    } catch (Error) {
        clearInterval(Step_Interval);
        Show_Error();
    }
};

const Render_Images = (Images) => {
    let Delay = 0;

    Images.forEach((Item) => {
        const Card = document.createElement('div');
        Card.className = 'Image_Card';
        Card.style.animationDelay = `${Delay}s`;

        const Img = document.createElement('img');
        Img.src = Item.thumbnail.source;
        Img.alt = Item.title;
        Img.className = 'Gallery_Image';
        Img.loading = 'lazy';

        const Overlay = document.createElement('div');
        Overlay.className = 'Image_Overlay';

        const Title = document.createElement('h3');
        Title.className = 'Image_Title';
        Title.textContent = Item.title;

        Overlay.appendChild(Title);
        Card.appendChild(Img);
        Card.appendChild(Overlay);

        Card.addEventListener('click', () => {
            window.open(Item.thumbnail.source, '_blank');
        });

        Image_Gallery.appendChild(Card);

        Delay += 0.05;
    });
};

const Show_Error = () => {
    Loader.classList.add('Hidden');
    Error_Message.classList.remove('Hidden');
};

const Handle_Search = () => {
    const Query = Search_Input.value;
    Fetch_Images(Query);
};

Search_Btn.addEventListener('click', Handle_Search);

Search_Input.addEventListener('keypress', (Event) => {
    if (Event.key === 'Enter') {
        Handle_Search();
    }
});

Search_Input.addEventListener('input', (Event) => {
    const Query = Event.target.value;

    if (Query.trim() === '') {
        Image_Gallery.innerHTML = '';
        Header.classList.remove('Active');
        Error_Message.classList.add('Hidden');
    }
});
