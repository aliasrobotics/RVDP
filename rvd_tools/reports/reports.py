# -*- coding: utf-8 -*-
#
# Alias Robotics SL
# https://aliasrobotics.com

"""
Class to generate PDF reports from tickets, both private or public
"""

from ..utils import cyan
import os
from ..importer.gitlab import *
import arrow


class Report:
    """
    Base report class
    """
    def __init__(self):
        pass

    def from_gitlab(self, id, deadline, disclose):
        """
        Generate a report from a Gitlab private archive
        """
        cyan("Creating temporary directory /tmp/rvd/reports/" + str(id) + " ...")
        temp_dir = "/tmp/rvd/reports/" + str(id)
        os.system("mkdir -p " + temp_dir)

        # Create the markdown file
        cyan("Creating Markdown file...")
        importer_private = GitlabImporter()
        flaw, labels = importer_private.get_flaw(id)
        markdown_content = ""
        markdown_content += '---' + "\n"
        markdown_content += 'title: "Robot Vulnerability advisory"' + "\n"
        markdown_content += 'author: [Alias Robotics (contact@aliasrobotics.com)]' + "\n"
        markdown_content += 'date: "' + str(arrow.utcnow().format('YYYY-MM-DD')) + '"' + "\n"
        markdown_content += 'toc: true' + "\n"
        markdown_content += 'subject: "Robot Cybersecurity"' + "\n"
        markdown_content += 'keywords: [Robotics, Security, Robot]' + "\n"
        markdown_content += 'subtitle: "Responsible notification about vulnerabilities discovered in one or several of your products."' + "\n"
        markdown_content += 'lang: "en"' + "\n"
        markdown_content += 'titlepage: true' + "\n"
        markdown_content += 'titlepage-color: "313131"' + "\n"
        markdown_content += 'titlepage-text-color: "FFFFFF"' + "\n"
        markdown_content += 'titlepage-rule-color: "FFFFFF"' + "\n"
        markdown_content += 'titlepage-rule-height: 1' + "\n"
        markdown_content += 'pandoc-latex-fontsize:' + "\n"
        markdown_content += '  - classes: [smallcontent]' + "\n"
        markdown_content += '    size: tiny' + "\n"
        markdown_content += '  - classes: [largecontent, important]' + "\n"
        markdown_content += '    size: huge' + "\n"
        markdown_content += 'bibliography: bibliography.bib' + "\n"
        markdown_content += '...' + "\n"
        markdown_content += '' + "\n"
        markdown_content += ' <!-- here goes the index -->' + "\n"
        markdown_content += '' + "\n"
        markdown_content += '\\newpage' + "\n"
        markdown_content += "\n"
        markdown_content += intro_content1
        if deadline:
            markdown_content += "`" + deadline + " days` " + "\n"
        else:
            markdown_content += "`" + "90 days" + "` " + "\n"
        markdown_content += intro_content2
        markdown_content += "\n"
        markdown_content += flaw.markdown(disclose)
        markdown_path = temp_dir + "/" + str(id) + ".md"
        markdown_file = open(markdown_path, 'w+')
        markdown_file.write(markdown_content)

        # Create the Makefile
        cyan("Creating Makefile...")
        makefile_path = temp_dir + "/Makefile"
        # makefile_content = "SOURCE_FILE := " + str(arrow.utcnow().format('YYYYMMDD')) + str(id) + ".md" + "\n"
        makefile_content = "SOURCE_FILE := " + str(id) + ".md" + "\n"
        makefile_content += "OUT_FILE := " + str(id) + "_report" + "\n"
        makefile_content += makefile
        makefile_file = open(makefile_path, 'w+')
        makefile_file.write(makefile_content)

        # Create LaTeX template
        cyan("Creating LaTeX template...")
        template_path = temp_dir + "/template.tex"
        template_content = eisvogel
        template_file = open(template_path, 'w+')
        template_file.write(template_content)

        # # Create the PDF report
        # os.system("cd " + str(temp_dir) + "; ls -l ; pwd ; make")

    def from_github(self, id):
        """
        Generate a report from official and public Github archive
        """
        raise NotImplementedError


intro_content1 = """\

# The advisory

On behalf of Alias Robotics, a robot cybersecurity company we'd like to inform
you by the present that vulnerabilities have been discovered in one of your
products.

In an attempt to avoid 0-days, our vulnerability policy for security flaws is to
notify product manufacturers and give them a maximum of 90 days to issue the fixes
starting the day of notification (today). This maximum deadline gets modified by
considering the severity of the flaw, the amount of systems deployed (in use)
and the risk that this flaw represents to society and the environment, among others.
Accordingly, for this flaw, *Alias Robotics grants a maximum of """


intro_content2 = """to issue the appropriate patches starting the day of notification """ + \
str("(today, " + arrow.utcnow().format('YYYY-MM-DD') + ").* ") + \
"""\

During this period, our team will not publicly disclose the contents of the
vulnerability found nor any related material that could
relate to it. We reserve the right to bring deadlines forwards or backwards
while we remain committed to treating all vendors strictly equally and
we expect to be held to the same standard.

In case you require further information or assistance to fix this (or these)
flaw/s, our security engineers would be happy to support you using their usual
hourly consulting rate. Moreover and provided that our team already found
security flaws in your product, we highly encourage you to consider performing
an in-depth security assessment. We offer such services at
https://aliasrobotics.com/services.html.

Do not hesitate to contact us if you have any questions.

Kind regards,

Alias Robotics Team

\\newpage
"""

makefile = """\
BUILDDIR := $(CURDIR)/build
EXTENSION := .pdf
PANDOC_TEMPLATE := $(CURDIR)/template.tex
PANDOC_OPTIONS := \
					--variable fontsize=10pt \
					--pdf-engine=xelatex \
					--filter pandoc-latex-fontsize \
					--template=$(PANDOC_TEMPLATE) $(SOURCE_FILE)
define exec_pandoc
	@echo "Building..."
	@pandoc $(PANDOC_OPTIONS) -o $(1)
	@echo "Build finished for $(1)"
endef
.PHONY: clean all debug
all: $(OUT_FILE)$(EXTENSION)
$(OUT_FILE)$(EXTENSION) : $(SOURCE_FILE) $(BUILDDIR) $(PANDOC_TEMPLATE)
	$(call exec_pandoc, $(OUT_FILE)$(EXTENSION))
$(BUILDDIR):
	@mkdir $(BUILDDIR)
debug: EXTENSION := .tex
debug: $(OUT_FILE)$(EXTENSION)
clean:
	@rm -rfv $(BUILDDIR)
	@rm -fv $(OUT_FILE)$(EXTENSION)
	$(eval EXTENSION := .tex)
	@rm -fv $(OUT_FILE)$(EXTENSION)

"""

eisvogel = r"""
%%
% Copyright (c) 2017 - 2019, Pascal Wagler;
% Copyright (c) 2014 - 2019, John MacFarlane
%
% All rights reserved.
%
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions
% are met:
%
% - Redistributions of source code must retain the above copyright
% notice, this list of conditions and the following disclaimer.
%
% - Redistributions in binary form must reproduce the above copyright
% notice, this list of conditions and the following disclaimer in the
% documentation and/or other materials provided with the distribution.
%
% - Neither the name of John MacFarlane nor the names of other
% contributors may be used to endorse or promote products derived
% from this software without specific prior written permission.
%
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
% "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
% LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
% FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
% COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
% INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
% BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
% LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
% CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
% LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
% ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
% POSSIBILITY OF SUCH DAMAGE.
%%

%%
% This is the Eisvogel pandoc LaTeX template.
%
% For usage information and examples visit the official GitHub page:
% https://github.com/Wandmalfarbe/pandoc-latex-template
%%

% Options for packages loaded elsewhere
\PassOptionsToPackage{unicode$for(hyperrefoptions)$,$hyperrefoptions$$endfor$}{hyperref}
\PassOptionsToPackage{hyphens}{url}
\PassOptionsToPackage{dvipsnames,svgnames*,x11names*,table}{xcolor}
$if(dir)$
$if(latex-dir-rtl)$
\PassOptionsToPackage{RTLdocument}{bidi}
$endif$
$endif$
%
\documentclass[
$if(fontsize)$
  $fontsize$,
$endif$
$if(lang)$
  $babel-lang$,
$endif$
$if(papersize)$
  $papersize$paper,
$else$
  a4paper,
$endif$
$if(beamer)$
  ignorenonframetext,
$if(handout)$
  handout,
$endif$
$if(aspectratio)$
  aspectratio=$aspectratio$,
$endif$
$endif$
$for(classoption)$
  $classoption$$sep$,
$endfor$
,tablecaptionabove
]{$if(beamer)$$documentclass$$else$$if(book)$scrbook$else$scrartcl$endif$$endif$}
$if(beamer)$
$if(background-image)$
\usebackgroundtemplate{%
  \includegraphics[width=\paperwidth]{$background-image$}%
}
$endif$
\usepackage{pgfpages}
\setbeamertemplate{caption}[numbered]
\setbeamertemplate{caption label separator}{: }
\setbeamercolor{caption name}{fg=normal text.fg}
\beamertemplatenavigationsymbols$if(navigation)$$navigation$$else$empty$endif$
$for(beameroption)$
\setbeameroption{$beameroption$}
$endfor$
% Prevent slide breaks in the middle of a paragraph
\widowpenalties 1 10000
\raggedbottom
$if(section-titles)$
\setbeamertemplate{part page}{
  \centering
  \begin{beamercolorbox}[sep=16pt,center]{part title}
    \usebeamerfont{part title}\insertpart\par
  \end{beamercolorbox}
}
\setbeamertemplate{section page}{
  \centering
  \begin{beamercolorbox}[sep=12pt,center]{part title}
    \usebeamerfont{section title}\insertsection\par
  \end{beamercolorbox}
}
\setbeamertemplate{subsection page}{
  \centering
  \begin{beamercolorbox}[sep=8pt,center]{part title}
    \usebeamerfont{subsection title}\insertsubsection\par
  \end{beamercolorbox}
}
\AtBeginPart{
  \frame{\partpage}
}
\AtBeginSection{
  \ifbibliography
  \else
    \frame{\sectionpage}
  \fi
}
\AtBeginSubsection{
  \frame{\subsectionpage}
}
$endif$
$endif$
$if(beamerarticle)$
\usepackage{beamerarticle} % needs to be loaded first
$endif$
$if(fontfamily)$
\usepackage[$for(fontfamilyoptions)$$fontfamilyoptions$$sep$,$endfor$]{$fontfamily$}
$else$
\usepackage{lmodern}
$endif$
$if(linestretch)$
\usepackage{setspace}
\setstretch{$linestretch$}
$else$
\usepackage{setspace}
\setstretch{1.2}
$endif$
\usepackage{amssymb,amsmath}
\usepackage{ifxetex,ifluatex}
\ifnum 0\ifxetex 1\fi\ifluatex 1\fi=0 % if pdftex
  \usepackage[$if(fontenc)$$fontenc$$else$T1$endif$]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage{textcomp} % provide euro and other symbols
\else % if luatex or xetex
$if(mathspec)$
  \ifxetex
    \usepackage{mathspec}
  \else
    \usepackage{unicode-math}
  \fi
$else$
  \usepackage{unicode-math}
$endif$
  \defaultfontfeatures{Scale=MatchLowercase}
  \defaultfontfeatures[\rmfamily]{Ligatures=TeX,Scale=1}
$if(mainfont)$
  \setmainfont[$for(mainfontoptions)$$mainfontoptions$$sep$,$endfor$]{$mainfont$}
$endif$
$if(sansfont)$
  \setsansfont[$for(sansfontoptions)$$sansfontoptions$$sep$,$endfor$]{$sansfont$}
$endif$
$if(monofont)$
  \setmonofont[$for(monofontoptions)$$monofontoptions$$sep$,$endfor$]{$monofont$}
$endif$
$for(fontfamilies)$
  \newfontfamily{$fontfamilies.name$}[$for(fontfamilies.options)$$fontfamilies.options$$sep$,$endfor$]{$fontfamilies.font$}
$endfor$
$if(mathfont)$
$if(mathspec)$
  \ifxetex
    \setmathfont(Digits,Latin,Greek)[$for(mathfontoptions)$$mathfontoptions$$sep$,$endfor$]{$mathfont$}
  \else
    \setmathfont[$for(mathfontoptions)$$mathfontoptions$$sep$,$endfor$]{$mathfont$}
  \fi
$else$
  \setmathfont[$for(mathfontoptions)$$mathfontoptions$$sep$,$endfor$]{$mathfont$}
$endif$
$endif$
$if(CJKmainfont)$
  \ifxetex
    \usepackage{xeCJK}
    \setCJKmainfont[$for(CJKoptions)$$CJKoptions$$sep$,$endfor$]{$CJKmainfont$}
  \fi
$endif$
$if(luatexjapresetoptions)$
  \ifluatex
    \usepackage[$for(luatexjapresetoptions)$$luatexjapresetoptions$$sep$,$endfor$]{luatexja-preset}
  \fi
$endif$
$if(CJKmainfont)$
  \ifluatex
    \usepackage[$for(luatexjafontspecoptions)$$luatexjafontspecoptions$$sep$,$endfor$]{luatexja-fontspec}
    \setmainjfont[$for(CJKoptions)$$CJKoptions$$sep$,$endfor$]{$CJKmainfont$}
  \fi
$endif$
\fi
$if(beamer)$
$if(theme)$
\usetheme[$for(themeoptions)$$themeoptions$$sep$,$endfor$]{$theme$}
$endif$
$if(colortheme)$
\usecolortheme{$colortheme$}
$endif$
$if(fonttheme)$
\usefonttheme{$fonttheme$}
$endif$
$if(mainfont)$
\usefonttheme{serif} % use mainfont rather than sansfont for slide text
$endif$
$if(innertheme)$
\useinnertheme{$innertheme$}
$endif$
$if(outertheme)$
\useoutertheme{$outertheme$}
$endif$
$endif$
% Use upquote if available, for straight quotes in verbatim environments
\IfFileExists{upquote.sty}{\usepackage{upquote}}{}
\IfFileExists{microtype.sty}{% use microtype if available
  \usepackage[$for(microtypeoptions)$$microtypeoptions$$sep$,$endfor$]{microtype}
  \UseMicrotypeSet[protrusion]{basicmath} % disable protrusion for tt fonts
}{}
$if(indent)$
$else$
\makeatletter
\@ifundefined{KOMAClassName}{% if non-KOMA class
  \IfFileExists{parskip.sty}{%
    \usepackage{parskip}
  }{% else
    \setlength{\parindent}{0pt}
    \setlength{\parskip}{6pt plus 2pt minus 1pt}}
}{% if KOMA class
  \KOMAoptions{parskip=half}}
\makeatother
$endif$
$if(verbatim-in-note)$
\usepackage{fancyvrb}
$endif$
\usepackage{xcolor}
\definecolor{default-linkcolor}{HTML}{A50000}
\definecolor{default-filecolor}{HTML}{A50000}
\definecolor{default-citecolor}{HTML}{4077C0}
\definecolor{default-urlcolor}{HTML}{4077C0}
\IfFileExists{xurl.sty}{\usepackage{xurl}}{} % add URL line breaks if available
\IfFileExists{bookmark.sty}{\usepackage{bookmark}}{\usepackage{hyperref}}
\hypersetup{
$if(title-meta)$
  pdftitle={$title-meta$},
$endif$
$if(author-meta)$
  pdfauthor={$author-meta$},
$endif$
$if(lang)$
  pdflang={$lang$},
$endif$
$if(subject)$
  pdfsubject={$subject$},
$endif$
$if(keywords)$
  pdfkeywords={$for(keywords)$$keywords$$sep$, $endfor$},
$endif$
$if(colorlinks)$
  colorlinks=true,
  linkcolor=$if(linkcolor)$$linkcolor$$else$default-linkcolor$endif$,
  filecolor=$if(filecolor)$$filecolor$$else$default-filecolor$endif$,
  citecolor=$if(citecolor)$$citecolor$$else$default-citecolor$endif$,
  urlcolor=$if(urlcolor)$$urlcolor$$else$default-urlcolor$endif$,
$else$
  hidelinks,
$endif$
  breaklinks=true,
  pdfcreator={LaTeX via pandoc with the Eisvogel template}}
\urlstyle{same} % disable monospaced font for URLs
$if(verbatim-in-note)$
\VerbatimFootnotes % allow verbatim text in footnotes
$endif$
$if(geometry)$
\usepackage[margin=2.5cm,includehead=true,includefoot=true,centering,$for(geometry)$$geometry$$sep$,$endfor$]{geometry}
$else$
  $if(beamer)$
  $else$
  \usepackage[margin=2.5cm,includehead=true,includefoot=true,centering]{geometry}
  $endif$
$endif$
$if(logo)$
\usepackage[export]{adjustbox}
\usepackage{graphicx}
$endif$
$if(beamer)$
\newif\ifbibliography
$endif$
$if(listings)$
\usepackage{listings}
\newcommand{\passthrough}[1]{#1}
\lstset{defaultdialect=[5.3]Lua}
\lstset{defaultdialect=[x86masm]Assembler}
$endif$
$if(listings-no-page-break)$
\usepackage{etoolbox}
\BeforeBeginEnvironment{lstlisting}{\par\noindent\begin{minipage}{\linewidth}}
\AfterEndEnvironment{lstlisting}{\end{minipage}\par\addvspace{\topskip}}
$endif$
$if(lhs)$
\lstnewenvironment{code}{\lstset{language=Haskell,basicstyle=\small\ttfamily}}{}
$endif$
$if(highlighting-macros)$
$highlighting-macros$

% Workaround/bugfix from jannick0.
% See https://github.com/jgm/pandoc/issues/4302#issuecomment-360669013)
% or https://github.com/Wandmalfarbe/pandoc-latex-template/issues/2
%
% Redefine the verbatim environment 'Highlighting' to break long lines (with
% the help of fvextra). Redefinition is necessary because it is unlikely that
% pandoc includes fvextra in the default template.
\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}

$endif$
$if(tables)$
\usepackage{longtable,booktabs}
$if(beamer)$
\usepackage{caption}
% Make caption package work with longtable
\makeatletter
\def\fnum@table{\tablename~\thetable}
\makeatother
$else$
% Correct order of tables after \paragraph or \subparagraph
\usepackage{etoolbox}
\makeatletter
\patchcmd\longtable{\par}{\if@noskipsec\mbox{}\fi\par}{}{}
\makeatother
% Allow footnotes in longtable head/foot
\IfFileExists{footnotehyper.sty}{\usepackage{footnotehyper}}{\usepackage{footnote}}
\makesavenoteenv{longtable}
$endif$
$endif$
$if(graphics)$
\usepackage{graphicx,grffile}
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\def\maxheight{\ifdim\Gin@nat@height>\textheight\textheight\else\Gin@nat@height\fi}
\makeatother
% Scale images if necessary, so that they will not overflow the page
% margins by default, and it is still possible to overwrite the defaults
% using explicit options in \includegraphics[width, height, ...]{}
\setkeys{Gin}{width=\maxwidth,height=\maxheight,keepaspectratio}
$endif$
$if(links-as-notes)$
% Make links footnotes instead of hotlinks:
\DeclareRobustCommand{\href}[2]{#2\footnote{\url{#1}}}
$endif$
$if(strikeout)$
\usepackage[normalem]{ulem}
% Avoid problems with \sout in headers with hyperref
\pdfstringdefDisableCommands{\renewcommand{\sout}{}}
$endif$
\setlength{\emergencystretch}{3em}  % prevent overfull lines
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
$if(numbersections)$
\setcounter{secnumdepth}{$if(secnumdepth)$$secnumdepth$$else$3$endif$}
$else$
\setcounter{secnumdepth}{-\maxdimen} % remove section numbering
$endif$
$if(beamer)$
$else$
$if(block-headings)$
% Make \paragraph and \subparagraph free-standing
\ifx\paragraph\undefined\else
  \let\oldparagraph\paragraph
  \renewcommand{\paragraph}[1]{\oldparagraph{#1}\mbox{}}
\fi
\ifx\subparagraph\undefined\else
  \let\oldsubparagraph\subparagraph
  \renewcommand{\subparagraph}[1]{\oldsubparagraph{#1}\mbox{}}
\fi
$endif$
$endif$
$if(pagestyle)$
\pagestyle{$pagestyle$}
$endif$

% Make use of float-package and set default placement for figures to H.
% The option H means 'PUT IT HERE' (as  opposed to the standard h option which means 'You may put it here if you like').
\usepackage{float}
\floatplacement{figure}{$if(float-placement-figure)$$float-placement-figure$$else$H$endif$}

$for(header-includes)$
$header-includes$
$endfor$
$if(lang)$
\ifxetex
  $if(mainfont)$
  $else$
  % See issue https://github.com/reutenauer/polyglossia/issues/127
  \renewcommand*\familydefault{\sfdefault}
  $endif$
  % Load polyglossia as late as possible: uses bidi with RTL langages (e.g. Hebrew, Arabic)
  \usepackage{polyglossia}
  \setmainlanguage[$polyglossia-lang.options$]{$polyglossia-lang.name$}
$for(polyglossia-otherlangs)$
  \setotherlanguage[$polyglossia-otherlangs.options$]{$polyglossia-otherlangs.name$}
$endfor$
\else
  \usepackage[shorthands=off,$for(babel-otherlangs)$$babel-otherlangs$,$endfor$main=$babel-lang$]{babel}
$if(babel-newcommands)$
  $babel-newcommands$
$endif$
\fi
$endif$
$if(dir)$
\ifxetex
  % Load bidi as late as possible as it modifies e.g. graphicx
  \usepackage{bidi}
\fi
\ifnum 0\ifxetex 1\fi\ifluatex 1\fi=0 % if pdftex
  \TeXXeTstate=1
  \newcommand{\RL}[1]{\beginR #1\endR}
  \newcommand{\LR}[1]{\beginL #1\endL}
  \newenvironment{RTL}{\beginR}{\endR}
  \newenvironment{LTR}{\beginL}{\endL}
\fi
$endif$
$if(natbib)$
\usepackage[$natbiboptions$]{natbib}
\bibliographystyle{$if(biblio-style)$$biblio-style$$else$plainnat$endif$}
$endif$
$if(biblatex)$
\usepackage[$if(biblio-style)$style=$biblio-style$,$endif$$for(biblatexoptions)$$biblatexoptions$$sep$,$endfor$]{biblatex}
$for(bibliography)$
\addbibresource{$bibliography$}
$endfor$
$endif$

$if(title)$
\title{$title$$if(thanks)$\thanks{$thanks$}$endif$}
$endif$
$if(subtitle)$
$if(beamer)$
$else$
\usepackage{etoolbox}
\makeatletter
\providecommand{\subtitle}[1]{% add subtitle to \maketitle
  \apptocmd{\@title}{\par {\large #1 \par}}{}{}
}
\makeatother
$endif$
\subtitle{$subtitle$}
$endif$
$if(author)$
\author{$for(author)$$author$$sep$ \and $endfor$}
$endif$
\date{$date$}
$if(beamer)$
$if(institute)$
\institute{$for(institute)$$institute$$sep$ \and $endfor$}
$endif$
$if(titlegraphic)$
\titlegraphic{\includegraphics{$titlegraphic$}}
$endif$
$if(logo)$
\logo{\includegraphics{$logo$}}
$endif$
$endif$



%%
%% added
%%

%
% language specification
%
% If no language is specified, use English as the default main document language.
%
$if(lang)$$else$
\ifnum 0\ifxetex 1\fi\ifluatex 1\fi=0 % if pdftex
  \usepackage[shorthands=off,$for(babel-otherlangs)$$babel-otherlangs$,$endfor$main=english]{babel}
$if(babel-newcommands)$
  $babel-newcommands$
$endif$
\else
  $if(mainfont)$
  $else$
  % Workaround for bug in Polyglossia that breaks `\familydefault` when `\setmainlanguage` is used.
  % See https://github.com/Wandmalfarbe/pandoc-latex-template/issues/8
  % See https://github.com/reutenauer/polyglossia/issues/186
  % See https://github.com/reutenauer/polyglossia/issues/127
  \renewcommand*\familydefault{\sfdefault}
  $endif$
  % load polyglossia as late as possible as it *could* call bidi if RTL lang (e.g. Hebrew or Arabic)
  \usepackage{polyglossia}
  \setmainlanguage[]{english}
$for(polyglossia-otherlangs)$
  \setotherlanguage[$polyglossia-otherlangs.options$]{$polyglossia-otherlangs.name$}
$endfor$
\fi
$endif$

%
% for the background color of the title page
%
$if(titlepage)$
\usepackage{pagecolor}
\usepackage{afterpage}
$endif$

%
% break urls
%
\PassOptionsToPackage{hyphens}{url}

%
% When using babel or polyglossia with biblatex, loading csquotes is recommended
% to ensure that quoted texts are typeset according to the rules of your main language.
%
\usepackage{csquotes}

%
% captions
%
\definecolor{caption-color}{HTML}{777777}
$if(beamer)$
$else$
\usepackage[font={stretch=1.2}, textfont={color=caption-color}, position=top, skip=4mm, labelfont=bf, singlelinecheck=false, justification=$if(caption-justification)$$caption-justification$$else$raggedright$endif$]{caption}
\setcapindent{0em}
$endif$

%
% blockquote
%
\definecolor{blockquote-border}{RGB}{221,221,221}
\definecolor{blockquote-text}{RGB}{119,119,119}
\usepackage{mdframed}
\newmdenv[rightline=false,bottomline=false,topline=false,linewidth=3pt,linecolor=blockquote-border,skipabove=\parskip]{customblockquote}
\renewenvironment{quote}{\begin{customblockquote}\list{}{\rightmargin=0em\leftmargin=0em}%
\item\relax\color{blockquote-text}\ignorespaces}{\unskip\unskip\endlist\end{customblockquote}}

%
% Source Sans Pro as the de­fault font fam­ily
% Source Code Pro for monospace text
%
% 'default' option sets the default
% font family to Source Sans Pro, not \sfdefault.
%
$if(mainfont)$
$else$
\usepackage[default]{sourcesanspro}
\usepackage{sourcecodepro}

% XeLaTeX specific adjustments for straight quotes: https://tex.stackexchange.com/a/354887
% This issue is already fixed (see https://github.com/silkeh/latex-sourcecodepro/pull/5) but the
% fix is still unreleased.
% TODO: Remove this workaround when the new version of sourcecodepro is released on CTAN.
\ifxetex
\makeatletter
\defaultfontfeatures[\ttfamily]
  { Numbers   = \sourcecodepro@figurestyle,
    Scale     = \SourceCodePro@scale,
    Extension = .otf }
\setmonofont
  [ UprightFont    = *-\sourcecodepro@regstyle,
    ItalicFont     = *-\sourcecodepro@regstyle It,
    BoldFont       = *-\sourcecodepro@boldstyle,
    BoldItalicFont = *-\sourcecodepro@boldstyle It ]
  {SourceCodePro}
\makeatother
\fi
$endif$

%
% heading color
%
\definecolor{heading-color}{RGB}{40,40,40}
$if(beamer)$
$else$
\addtokomafont{section}{\color{heading-color}}
$endif$
% When using the classes report, scrreprt, book,
% scrbook or memoir, uncomment the following line.
%\addtokomafont{chapter}{\color{heading-color}}

%
% variables for title and author
%
$if(beamer)$
$else$
\usepackage{titling}
\title{$title$}
\author{$for(author)$$author$$sep$, $endfor$}
$endif$

%
% tables
%
$if(tables)$

\definecolor{table-row-color}{HTML}{F5F5F5}
\definecolor{table-rule-color}{HTML}{999999}

%\arrayrulecolor{black!40}
\arrayrulecolor{table-rule-color}     % color of \toprule, \midrule, \bottomrule
\setlength\heavyrulewidth{0.3ex}      % thickness of \toprule, \bottomrule
\renewcommand{\arraystretch}{1.3}     % spacing (padding)

% Reset rownum counter so that each table
% starts with the same row colors.
% https://tex.stackexchange.com/questions/170637/restarting-rowcolors
\let\oldlongtable\longtable
\let\endoldlongtable\endlongtable
\renewenvironment{longtable}{
\rowcolors{3}{}{table-row-color!100}  % row color
\oldlongtable} {
\endoldlongtable
\global\rownum=0\relax}

% Unfortunately the colored cells extend beyond the edge of the
% table because pandoc uses @-expressions (@{}) like so:
%
% \begin{longtable}[]{@{}ll@{}}
% \end{longtable}
%
% https://en.wikibooks.org/wiki/LaTeX/Tables#.40-expressions
$endif$

%
% remove paragraph indention
%
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt plus 2pt minus 1pt}
\setlength{\emergencystretch}{3em}  % prevent overfull lines

%
%
% Listings
%
%

$if(listings)$

%
% general listing colors
%
\definecolor{listing-background}{HTML}{F7F7F7}
\definecolor{listing-rule}{HTML}{B3B2B3}
\definecolor{listing-numbers}{HTML}{B3B2B3}
\definecolor{listing-text-color}{HTML}{000000}
\definecolor{listing-keyword}{HTML}{435489}
\definecolor{listing-keyword-2}{HTML}{1284CA} % additional keywords
\definecolor{listing-keyword-3}{HTML}{9137CB} % additional keywords
\definecolor{listing-identifier}{HTML}{435489}
\definecolor{listing-string}{HTML}{00999A}
\definecolor{listing-comment}{HTML}{8E8E8E}

\lstdefinestyle{eisvogel_listing_style}{
  language         = java,
$if(listings-disable-line-numbers)$
  xleftmargin      = 0.6em,
  framexleftmargin = 0.4em,
$else$
  numbers          = left,
  xleftmargin      = 2.7em,
  framexleftmargin = 2.5em,
$endif$
  backgroundcolor  = \color{listing-background},
  basicstyle       = \color{listing-text-color}\linespread{1.0}\small\ttfamily{},
  breaklines       = true,
  frame            = single,
  framesep         = 0.19em,
  rulecolor        = \color{listing-rule},
  frameround       = ffff,
  tabsize          = 4,
  numberstyle      = \color{listing-numbers},
  aboveskip        = 1.0em,
  belowskip        = 0.1em,
  abovecaptionskip = 0em,
  belowcaptionskip = 1.0em,
  keywordstyle     = {\color{listing-keyword}\bfseries},
  keywordstyle     = {[2]\color{listing-keyword-2}\bfseries},
  keywordstyle     = {[3]\color{listing-keyword-3}\bfseries\itshape},
  sensitive        = true,
  identifierstyle  = \color{listing-identifier},
  commentstyle     = \color{listing-comment},
  stringstyle      = \color{listing-string},
  showstringspaces = false,
  escapeinside     = {/*@}{@*/}, % Allow LaTeX inside these special comments
  literate         =
  {á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
  {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
  {à}{{\`a}}1 {è}{{\'e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1
  {À}{{\`A}}1 {È}{{\'E}}1 {Ì}{{\`I}}1 {Ò}{{\`O}}1 {Ù}{{\`U}}1
  {ä}{{\"a}}1 {ë}{{\"e}}1 {ï}{{\"i}}1 {ö}{{\"o}}1 {ü}{{\"u}}1
  {Ä}{{\"A}}1 {Ë}{{\"E}}1 {Ï}{{\"I}}1 {Ö}{{\"O}}1 {Ü}{{\"U}}1
  {â}{{\^a}}1 {ê}{{\^e}}1 {î}{{\^i}}1 {ô}{{\^o}}1 {û}{{\^u}}1
  {Â}{{\^A}}1 {Ê}{{\^E}}1 {Î}{{\^I}}1 {Ô}{{\^O}}1 {Û}{{\^U}}1
  {œ}{{\oe}}1 {Œ}{{\OE}}1 {æ}{{\ae}}1 {Æ}{{\AE}}1 {ß}{{\ss}}1
  {ç}{{\c c}}1 {Ç}{{\c C}}1 {ø}{{\o}}1 {å}{{\r a}}1 {Å}{{\r A}}1
  {€}{{\EUR}}1 {£}{{\pounds}}1 {«}{{\guillemotleft}}1
  {»}{{\guillemotright}}1 {ñ}{{\~n}}1 {Ñ}{{\~N}}1 {¿}{{?`}}1
  {…}{{\ldots}}1 {≥}{{>=}}1 {≤}{{<=}}1 {„}{{\glqq}}1 {“}{{\grqq}}1
  {”}{{''}}1
}
\lstset{style=eisvogel_listing_style}

\lstdefinelanguage{XML}{
  morestring      = [b]",
  moredelim       = [s][\bfseries\color{listing-keyword}]{<}{\ },
  moredelim       = [s][\bfseries\color{listing-keyword}]{</}{>},
  moredelim       = [l][\bfseries\color{listing-keyword}]{/>},
  moredelim       = [l][\bfseries\color{listing-keyword}]{>},
  morecomment     = [s]{<?}{?>},
  morecomment     = [s]{<!--}{-->},
  commentstyle    = \color{listing-comment},
  stringstyle     = \color{listing-string},
  identifierstyle = \color{listing-identifier}
}
$endif$

%
% header and footer
%
$if(beamer)$
$else$
$if(disable-header-and-footer)$
$else$
\usepackage{fancyhdr}

\fancypagestyle{eisvogel-header-footer}{
  \fancyhead{}
  \fancyfoot{}
  \lhead[$if(header-right)$$header-right$$else$$date$$endif$]{$if(header-left)$$header-left$$else$$title$$endif$}
  \chead[$if(header-center)$$header-center$$else$$endif$]{$if(header-center)$$header-center$$else$$endif$}
  \rhead[$if(header-left)$$header-left$$else$$title$$endif$]{$if(header-right)$$header-right$$else$$date$$endif$}
  \lfoot[$if(footer-right)$$footer-right$$else$\thepage$endif$]{$if(footer-left)$$footer-left$$else$$for(author)$$author$$sep$, $endfor$$endif$}
  \cfoot[$if(footer-center)$$footer-center$$else$$endif$]{$if(footer-center)$$footer-center$$else$$endif$}
  \rfoot[$if(footer-left)$$footer-left$$else$$for(author)$$author$$sep$, $endfor$$endif$]{$if(footer-right)$$footer-right$$else$\thepage$endif$}
  \renewcommand{\headrulewidth}{0.4pt}
  \renewcommand{\footrulewidth}{0.4pt}
}
\pagestyle{eisvogel-header-footer}
$endif$
$endif$

%%
%% end added
%%

\begin{document}

%%
%% begin titlepage
%%
$if(beamer)$
$else$
$if(titlepage)$
\begin{titlepage}
\newgeometry{left=6cm}
$if(titlepage-color)$
\definecolor{titlepage-color}{HTML}{$titlepage-color$}
\newpagecolor{titlepage-color}\afterpage{\restorepagecolor}
$endif$
\newcommand{\colorRule}[3][black]{\textcolor[HTML]{#1}{\rule{#2}{#3}}}
\begin{flushleft}
\noindent
\\[-1em]
\color[HTML]{$if(titlepage-text-color)$$titlepage-text-color$$else$5F5F5F$endif$}
\makebox[0pt][l]{\colorRule[$if(titlepage-rule-color)$$titlepage-rule-color$$else$435488$endif$]{1.3\textwidth}{$if(titlepage-rule-height)$$titlepage-rule-height$$else$4$endif$pt}}
\par
\noindent

{ \setstretch{1.4}
\vfill
\noindent {\huge \textbf{\textsf{$title$}}}
$if(subtitle)$
\vskip 1em
{\Large \textsf{$subtitle$}}
$endif$
\vskip 2em
\noindent
{\Large \textsf{$for(author)$$author$$sep$, $endfor$}
\vfill
}

$if(logo)$
\noindent
\includegraphics[width=$if(logo-width)$$logo-width$$else$100$endif$pt, left]{$logo$}
$endif$

\textsf{$date$}}
\end{flushleft}
\end{titlepage}
\restoregeometry
$endif$
$endif$

%%
%% end titlepage
%%

$if(has-frontmatter)$
\frontmatter
$endif$
$if(title)$
$if(beamer)$
\frame{\titlepage}
$endif$
$if(abstract)$
\begin{abstract}
$abstract$
\end{abstract}
$endif$
$endif$

$if(first-chapter)$
\setcounter{chapter}{$first-chapter$}
\addtocounter{chapter}{-1}
$endif$

$for(include-before)$
$include-before$

$endfor$
$if(toc)$
$if(toc-title)$
\renewcommand*\contentsname{$toc-title$}
$endif$
$if(beamer)$
\begin{frame}
$if(toc-title)$
  \frametitle{$toc-title$}
$endif$
  \tableofcontents[hideallsubsections]
\end{frame}
$if(toc-own-page)$
\newpage
$endif$
$else$
{
$if(colorlinks)$
\hypersetup{linkcolor=$if(toccolor)$$toccolor$$else$$endif$}
$endif$
\setcounter{tocdepth}{$if(toc-depth)$$toc-depth$$else$3$endif$}
\tableofcontents
$if(toc-own-page)$
\newpage
$endif$
}
$endif$
$endif$
$if(lot)$
\listoftables
$endif$
$if(lof)$
\listoffigures
$endif$
$if(linestretch)$
\setstretch{$linestretch$}
$endif$
$if(has-frontmatter)$
\mainmatter
$endif$
$body$

$if(has-frontmatter)$
\backmatter
$endif$
$if(natbib)$
$if(bibliography)$
$if(biblio-title)$
$if(has-chapters)$
\renewcommand\bibname{$biblio-title$}
$else$
\renewcommand\refname{$biblio-title$}
$endif$
$endif$
$if(beamer)$
\begin{frame}[allowframebreaks]{$biblio-title$}
  \bibliographytrue
$endif$
  \bibliography{$for(bibliography)$$bibliography$$sep$,$endfor$}
$if(beamer)$
\end{frame}
$endif$

$endif$
$endif$
$if(biblatex)$
$if(beamer)$
\begin{frame}[allowframebreaks]{$biblio-title$}
  \bibliographytrue
  \printbibliography[heading=none]
\end{frame}
$else$
\printbibliography$if(biblio-title)$[title=$biblio-title$]$endif$
$endif$

$endif$
$for(include-after)$
$include-after$

$endfor$
\end{document}

"""
