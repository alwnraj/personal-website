import datetime
import pathlib
from fasthtml.common import *
from fh_bootstrap import bst_hdrs, Container, Image, Icon, ContainerT
from markdown import markdown
import frontmatter
from starlette.responses import PlainTextResponse

headers = (
    Link(
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
        rel="stylesheet",
        type="text/css",
    ),
    Link(  # Add the favicon link
        rel="icon",
        type="image/jpeg",
        href="/assets/logo.jpg",
    ),
    # Meta tag for description
    Meta(name="description", content="Welcome to Alwin Rajkumar's personal site, where you can find blog posts, resume, and more about my projects."),
    StyleX("assets/styles.css"),
    
    *Socials(title="Alwin Rajkumar", description="Alwin's Personal Site", site_name="Alwin's Personal Site", image="assets/profile_picture.jpeg", url="https://personal-website-cyan-omega.vercel.app/"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, viewport-fit=cover"),
    Meta(charset="utf-8"),
)


async def not_found(request, exc):
    return RedirectResponse(url="/")


exception_handlers = {
    404: not_found
}

app = FastHTML(hdrs=bst_hdrs + headers, live=False, default_hdrs=False, exception_handlers=exception_handlers)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/posts/img", StaticFiles(directory="posts/img"), name="posts_img")


def get_base(content):
    return (
        Title("Alwin Rajkumar"),
        Container(
            Nav(
                Div(
                    A("Home", href="/", cls="nav-link"),
                    A("Resume",href="/assets/Resume.pdf", cls="nav-link", target="_blank"),
                    A("Posts", href="/posts", cls="nav-link"),
                    #A("Papers", href="/papers", cls="nav-link"),
                    cls="nav-links",
                ),
                cls="navbar",
            ),
            Div(
                Image(
                    "/assets/profile_picture.jpeg",
                    alt="Alwin Rajkumar",
                    cls="profile-image",
                ),
                Div(
                    H1("Alwin Rajkumar"),
                    P("University of Louisville | Computer Science & Engineering"),
                    Div(
                        #Icon("fab fa-x-twitter fa-sm", href="www.twitter.com/xceron_", button=False),
                        Icon("fab fa-github fa-sm", href="https://github.com/alwnraj?tab=overview&from=2024-07-01&to=2024-07-04", button=False),
                        Icon("fab fa-linkedin fa-sm", href="https://www.linkedin.com/in/alwin-rajkumar-3734a12ab/",
                             button=False),
                        #Icon("fab fa-discord fa-sm", href="https://discord.com/users/1233745701243195433",
                             #button=False),
                        Icon("fas fa-at fa-sm", href="mailto:alwin.rajkumar@louisville.edu", button=False),
                        cls="social-icons",
                    ),
                    cls="profile-info",
                ),
                cls="profile",
            ),
            Div(
                content,
                cls="content",
            ),
            typ=ContainerT.Sm,
        )
    )

    


md_exts = ('codehilite', 'smarty', 'extra', 'attr_list', 'toc')


def Markdown(s, exts=md_exts, **kw):
    # https://github.com/AnswerDotAI/fh-about/blob/7e5109c26ba2f4fcba897cc83add6ee74621ed20/app.py#L6
    return Div(NotStr(markdown(s, extensions=exts)), **kw)


@app.get("/")
def home():
    with open('main.md', 'r') as file:
        content = file.read()
    return get_base(Markdown(content))


@app.get("/posts/")
def posts():
    blog_dir = pathlib.Path("posts")
    blog_files = [file.stem for file in blog_dir.glob("*.md")]
    links = []
    for file in blog_files:
        with open(f"posts/{file}.md", 'r') as post_file:
            content = frontmatter.load(post_file)
            if not content["draft"]:
                links.append(Li(content["date"], A(content["title"], href=f"/posts/{file}")))
    return get_base(Div(H2("Posts"), Ul(*links)))


@app.get("/posts/{post}")
def get_post(post: str):
    post_path = pathlib.Path(f"posts/{post}.md")
    if not post_path.exists():
        return RedirectResponse(url="/")
    
    md_file = frontmatter.load(post_path)
    if md_file["draft"]:
        return RedirectResponse(url="/")

    # Custom meta description for blog posts
    post_description = md_file.get("description", "Read more about this post on Alwin Rajkumar's personal blog.")
    
    custom_headers = headers + (
        Meta(name="description", content=post_description),
    )
    
    return get_base(Markdown(md_file.content))


# Function to generate the sitemap XML
@app.get("/sitemap.xml")
def sitemap():
    # Your sitemap content goes here (this is just an example)
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://personal-website-cyan-omega.vercel.app/</loc>
            <lastmod>2024-10-16</lastmod>
            <priority>1.00</priority>
        </url>
        <url>
            <loc>https://personal-website-cyan-omega.vercel.app/posts</loc>
            <lastmod>2024-10-16</lastmod>
            <priority>0.80</priority>
        </url>
    </urlset>
    """
    
    return PlainTextResponse(content=xml_content, media_type="application/xml")


'''@app.get("/papers/")
def papers():
    return get_base(
        (H2("Papers"),
         Div(
             H3("2024"),
             Ul(
                 Li("Large Language Models as Knowledge Engineers",
                    Br(),
                    Span("[",
                         A("PDF",
                           href="https://www.wi2.uni-trier.de/shared/publications/2024_ICCBR-WS_LLMInCBR_BrandEtAl.pdf")),
                    "]",
                    Span("[", A("DBLP", href="https://dblp.org/rec/conf/iccbr/BrandMB24.html")), "]"),
             ),
             H3("2023"),
             Ul(
             Li("Using Deep Reinforcement Learning for the Adaptation of Semantic Workflows",
                    Br(),
                    Span("[",
                         A("PDF",
                           href="http://www.wi2.uni-trier.de/shared/publications/2023_Brand_RLForAdaptiveWorkflows.pdf")),
                    "]",
                    Span("[",
                         A("DBLP", href="https://dblp.org/rec/conf/iccbr/BrandLM0B23.html")), "]"),
                 Li("Adaptive Management of Cyber-Physical Workflows by Means of Case-Based Reasoning and Automated Planning",
                    Br(),
                    Span("[",
                         A("PDF",
                           href="http://www.wi2.uni-trier.de/shared/publications/2023_EDOC_MalburgEtAl_AdaptiveWorkflows_by_CBR_and_Planning.pdf")),
                    "]",
                    Span("[",
                         A("DBLP", href="https://dblp.org/rec/conf/edoc/MalburgBB22")),
                    "]"
                    )
             )
         ))
    )
    '''



if __name__ == "__main__":
    serve(host="0.0.0.0", port=5001)