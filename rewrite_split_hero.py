import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update favicons and meta tags to use exact .PNG (case-sensitive as user typed)
html = re.sub(
    r'<link rel="icon" type="image/[^"]+" href="[^"]+">',
    '<link rel="icon" type="image/png" href="./assets/ICON RP.PNG">',
    html
)
html = re.sub(
    r'<meta property="og:image" content="[^"]+">',
    '<meta property="og:image" content="https://www.rainbowpolypack.com/assets/FINAL LOGO.PNG">',
    html
)
html = re.sub(
    r'<meta property="twitter:image" content="[^"]+">',
    '<meta property="twitter:image" content="https://www.rainbowpolypack.com/assets/FINAL LOGO.PNG">',
    html
)
html = html.replace(
    '"image": "https://www.rainbowpolypack.com/assets/logo_assets/svg/polypack-logo-transparent-bg.svg"',
    '"image": "https://www.rainbowpolypack.com/assets/FINAL LOGO.PNG"'
)
html = html.replace(
    '"logo": "https://www.rainbowpolypack.com/assets/logo_assets/svg/polypack-logo-transparent-bg.svg"',
    '"logo": "https://www.rainbowpolypack.com/assets/FINAL LOGO.PNG"'
)
html = html.replace(
    '"url": "https://www.rainbowpolypack.com/assets/logo_assets/svg/polypack-logo-transparent-bg.svg"',
    '"url": "https://www.rainbowpolypack.com/assets/FINAL LOGO.PNG"'
)
# Make sure we didn't leave any stray icon references
html = html.replace('./assets/ICON RP.jpg', './assets/ICON RP.PNG')
html = html.replace('./assets/ICON RP.png', './assets/ICON RP.PNG')

# 2. Rewrite Navbar and Home (carefully bounding them)
navbar_start = html.find('    function Navbar() {')
home_start = html.find('    function Home() {')
product_card_start = html.find('    function ProductCard({ p }) {')

if navbar_start == -1 or home_start == -1 or product_card_start == -1:
    raise Exception("Could not find start index for Navbar, Home, or ProductCard!")

navbar_code = """    function Navbar() {
      const { t } = useLanguage();
      const [isOpen, setIsOpen] = useState(false);
      const [scrolled, setScrolled] = useState(false);
      const location = useLocation();
      const navigate = useNavigate();

      useEffect(() => {
        const handleScroll = () => {
          setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
      }, []);

      const links = [
        { path: '/', label: t("nav_home") },
        { path: '/about', label: t("nav_about") },
        { path: '/#products', label: t("nav_products") },
        { path: '/sustainability', label: t("nav_sustainability") || "Sustainability" }
      ];

      const handleNav = (path) => {
        setIsOpen(false);
        if (path.startsWith('/#')) {
          const targetId = path.substring(2);
          if (location.pathname !== '/') {
            navigate('/');
            setTimeout(() => {
              document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
          } else {
            document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' });
          }
        } else {
          navigate(path);
          window.scrollTo(0, 0);
        }
      };

      const waText = encodeURIComponent("Hello Rainbow Polypack Team, I am interested in your PET preforms.");
      const waLink = `https://wa.me/918735817667?text=${waText}`;
      
      return html`
        <header className=${`fixed top-0 left-0 right-0 z-[60] transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm border-b border-slate-100 py-3' : 'bg-transparent py-6'}`}>
          <div className="max-w-7xl mx-auto px-6 lg:px-8 flex items-center justify-between">
            <div
              onClick=${() => navigate('/')}
              className="cursor-pointer transition-transform duration-300 hover:scale-[1.02]"
            >
              <img src="./assets/FINAL LOGO.PNG" width="200" height="60" className=${`w-auto object-contain transition-all duration-300 ${scrolled ? 'h-10' : 'h-14'}`} style=${{ mixBlendMode: 'multiply' }} alt="Rainbow Polypack Logo" onError=${(e) => { e.target.onerror = null; e.target.style.display = 'none'; }} />
            </div>

            <!-- Desktop Inline Links -->
            <div className="hidden md:flex items-center gap-8">
              ${links.map(link => {
                const isActive = (link.path === '/' && location.pathname === '/' && !location.hash) || 
                                 (link.path !== '/' && (location.pathname + location.hash) === link.path);
                return html`
                <div
                  key=${link.path}
                  onClick=${() => handleNav(link.path)}
                  className=${`relative cursor-pointer text-sm font-bold uppercase tracking-wider transition-colors ${isActive ? 'text-brand-green' : 'text-slate-600 hover:text-brand-black'}`}
                >
                  ${link.label}
                  ${isActive ? html`<div className="absolute -bottom-1 left-0 w-full h-0.5 bg-brand-green rounded-full"></div>` : ''}
                </div>
              `})}
              <${Link} 
                to="/brochure" 
                className="bg-brand-green text-white rounded-lg px-6 py-2.5 font-bold text-sm tracking-wider uppercase hover:bg-brand-black transition-colors shadow-sm"
              >
                ${t("nav_enquiry")}
              <//>
            </div>

            <!-- Mobile Burger Menu -->
            <div className="flex md:hidden items-center gap-4">
              <${Link} 
                to="/brochure" 
                className="bg-brand-green text-white rounded-lg px-4 py-2 font-bold text-xs tracking-wider uppercase shadow-sm"
              >
                Enquire
              <//>
              <button
                onClick=${() => setIsOpen(!isOpen)}
                aria-label="Toggle Menu"
                className="text-slate-800 p-2"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d=${isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}></path>
                </svg>
              </button>
            </div>
          </div>
        </header>

        <!-- Mobile Open Menu Dropdown -->
        <${AnimatePresence}>
          ${isOpen && html`
            <${motion.div}
              initial=${{ opacity: 0, y: -10 }}
              animate=${{ opacity: 1, y: 0 }}
              exit=${{ opacity: 0, y: -10 }}
              className="fixed top-[70px] left-4 right-4 z-[50] md:hidden bg-white border border-slate-100 rounded-xl overflow-hidden shadow-md"
            >
              <div className="p-4 space-y-1">
                ${links.map(link => {
                  const isActive = (link.path === '/' && location.pathname === '/' && !location.hash) || 
                                   (link.path !== '/' && (location.pathname + location.hash) === link.path);
                  return html`
                  <div
                    key=${link.path}
                    onClick=${() => handleNav(link.path)}
                    className=${`cursor-pointer block px-4 py-3 rounded-lg text-sm font-bold transition-colors ${isActive ? 'bg-brand-green/10 text-brand-green' : 'text-slate-600 hover:bg-slate-50'}`}
                  >
                    ${link.label}
                  </div>
                `})}
              </div>
            <//>
          `}
        <//>
      `;
    }
"""

home_code = """    function Home() {
      const { t } = useLanguage();
      const mobileVideoRef = useRef(null);

      useEffect(() => {
        window.scrollTo(0, 0);
        document.title = "Rainbow Polypack | Premium PET Preform Manufacturers | Chhatral, Gujarat";
      }, []);

      const features = [
        {
          id: 1,
          title: "Rigorous Quality Assurance",
          desc: "Our preforms are manufactured under stringent quality control protocols, ensuring every batch meets the precise dimensional tolerances required for high-speed blowing lines.",
          icon: html`<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
        },
        {
          id: 2,
          title: "100% Hot Runner Tooling",
          desc: "We utilize advanced hot runner moulds for gate-vestige elimination and optimal optical clarity, removing the risks associated with cold-runner recycled defects.",
          icon: html`<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>`
        },
        {
          id: 3,
          title: "High-Precision Tolerances",
          desc: "Guaranteed weight variances of ±0.15g per preform. Our injection molding infrastructure provides identical wall distribution for uniform stretching.",
          icon: html`<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"></path></svg>`
        },
        {
          id: 4,
          title: "Streamlined Supply Chain",
          desc: "Experience direct-to-manufacturer procurement. Our flat organizational structure means faster quotation turnarounds and priority production queueing.",
          icon: html`<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>`
        },
        {
          id: 5,
          title: "The B2B Standard",
          desc: "Trusted by leading FMCG and edible oil brands across India. We deliver commercial-scale preform volumes without compromising on consistency.",
          icon: html`<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>`
        }
      ];

      return html`
        <div className="bg-brand-white w-full font-sans text-slate-800">
          
          <!-- Corporate Split-Hero Section -->
          <div className="relative pt-32 pb-16 md:pt-40 md:pb-24 px-6 max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
              
              <!-- Left Column: Copy & CTA -->
              <div className="flex flex-col text-left order-2 lg:order-1">
                <div className="inline-block px-4 py-1.5 rounded-md bg-slate-100 text-slate-700 font-bold text-xs uppercase tracking-widest mb-6 w-fit border border-slate-200">ISO 9001:2015 Certified</div>
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-black text-brand-black tracking-tight mb-6 leading-[1.1]">
                  Premium PET Preform <br className="hidden md:block" /> Manufacturing
                </h1>
                <p className="text-lg text-slate-600 max-w-xl mb-10 font-medium leading-relaxed">
                  High-performance CTC 29/21mm preforms engineered with 100% Hot Runner Moulds for FMCG, edible oil, and liquid packaging brands across India.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
                  <${Link} to="/brochure" className="px-8 py-4 bg-brand-green text-white rounded-lg font-bold text-base hover:bg-brand-black transition-colors shadow-sm flex items-center justify-center">
                    Request a Technical Quote
                  <//>
                  <a href="#products" className="px-8 py-4 bg-white text-brand-black border border-slate-200 rounded-lg font-bold text-base hover:bg-slate-50 transition-colors shadow-sm flex items-center justify-center">
                    View Catalog
                  </a>
                </div>
              </div>
              
              <!-- Right Column: Inline Video -->
              <div className="relative w-full order-1 lg:order-2 flex justify-center">
                <div className="relative w-full max-w-lg lg:max-w-full rounded-xl overflow-hidden shadow-md bg-brand-black aspect-video border border-slate-200">
                  <video 
                    ref=${mobileVideoRef}
                    src="./assets/mobile-bg.mp4" 
                    muted 
                    autoPlay 
                    loop 
                    playsInline 
                    preload="none"
                    poster="./assets/frames/preform_mould_frames_1080p_webp/fram00001.webp"
                    className="w-full h-full object-cover"
                  ></video>
                </div>
              </div>
              
            </div>
          </div>

          <!-- Seamless Transition via Alternating Backgrounds -->
          <!-- Engineering Excellence Grid Section -->
          <div className="bg-slate-50 py-24 border-y border-slate-200/60">
            <div className="max-w-7xl mx-auto px-6">
              <div className="text-left mb-16 max-w-3xl">
                <h2 className="text-3xl md:text-4xl font-black text-brand-black mb-4 tracking-tight">Engineering Excellence</h2>
                <p className="text-slate-600 text-lg">Our state-of-the-art facility guarantees commercial-scale production with precision tolerances, empowering your blowing lines.</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${features.map(feature => html`
                  <div key=${feature.id} className="p-8 rounded-xl bg-white border border-slate-200 shadow-sm hover:shadow-md transition-shadow duration-300">
                    <div className="text-brand-green mb-6 bg-slate-50 w-14 h-14 rounded-lg flex items-center justify-center border border-slate-100">
                      ${feature.icon}
                    </div>
                    <h3 className="text-lg font-bold text-brand-black mb-3">${feature.title}</h3>
                    <p className="text-slate-600 leading-relaxed text-sm">${feature.desc}</p>
                  </div>
                `)}
              </div>
            </div>
          </div>
          
          <!-- B2B Product Catalog -->
          <${Products} isIntegrated=${true} />
        </div>
      `;
    }
"""

# Apply the replacement carefully!
html_first_half = html[:navbar_start] + navbar_code + "\n"
html_second_half = html[home_start:]
html = html_first_half + html_second_half

home_start_new = html.find('    function Home() {')
product_card_start_new = html.find('    function ProductCard({ p }) {')

html = html[:home_start_new] + home_code + "\n" + html[product_card_start_new:]

# 3. Replace Footer Logo & styling to use FONTs.PNG exactly as requested
# and apply mix-blend-multiply
html = re.sub(
    r'<img src="\./assets/logo_assets/svg/polypack-logo-transparent-bg\.svg"[^>]+>',
    '<img src="./assets/FONTs.PNG" width="600" height="200" className="w-64 sm:w-80 h-auto opacity-90 object-contain mx-auto" style={{ mixBlendMode: \'multiply\' }} alt="Rainbow Polypack Logo" onError={(e) => { e.target.onerror = null; e.target.style.display = \'none\'; }} />',
    html
)
# Make sure old .jpg paths are removed if they exist
html = html.replace('./assets/FINAL LOGO.jpg', './assets/FINAL LOGO.PNG')
html = html.replace('./assets/FONTs.jpg', './assets/FONTs.PNG')

# 4. Sharpen Aesthetics globally in the remaining code:
# Replace rounded-3xl and rounded-[2.5rem] with rounded-xl or rounded-lg
html = html.replace('rounded-3xl', 'rounded-xl')
html = html.replace('rounded-2xl', 'rounded-lg')
html = html.replace('rounded-[2.5rem]', 'rounded-xl')

# Replace aggressive shadows with subtle ones
html = html.replace('shadow-2xl', 'shadow-md')
html = html.replace('shadow-[0_20px_50px_rgba(112,164,67,0.5)]', 'shadow-sm')
html = html.replace('shadow-[0_15px_30px_rgba(112,164,67,0.4)]', 'shadow-sm')
html = html.replace('shadow-[0_15px_30px_rgba(11,11,12,0.4)]', 'shadow-sm')
html = html.replace('shadow-[0_20px_40px_rgba(0,0,0,0.1)]', 'shadow-md')

# Ensure seamless transitions by updating borders in Products component
html = html.replace('bg-brand-white relative overflow-hidden  pt-12', 'bg-white relative overflow-hidden pt-12')
# Make sure tabular-nums are not destroyed if they existed, though this was reverted

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
