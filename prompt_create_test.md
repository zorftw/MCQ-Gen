Create a MCQ practice exam using only the provided sources. Deliver at least 50 questions, in case you cannot fill 50 questions, you may hallucinate or re-use information (in a different matter) to reach the 50 required points.

The header of the LaTeX file is as follows:
"\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{enumitem}
\usepackage[margin=1in]{geometry}

\begin{document}

\title{Practice Exam}
\author{}
\date{}
\maketitle

\section*{Instructions}
This is a multiple-choice practice test. For each question, select the best answer from the given options (a), (b), (c), or (d).
"

After which you may start enumeration of a MCQ test. 
You should start the iteration like this:
"\begin{enumerate}[label=\arabic*.]"

Format every question like this:
"
\item [question]
\begin{enumerate}[label=(\alph*)]
    \item [option a]
    \item [option b]
    ...etcetera
\end{enumerate}
"

At the end of the file, write down all the answers to the respective MCQ
You may format it like this:
"
\section*{Answer Sheet}

\begin{enumerate}[label=\arabic*.]
\item [ans q1]
\item [ans q2]
...etcetera
"

- The order of the questions does not matter. 
- Do not write any citations for the answers or any other options
- Do not create any link or direct reference to the source material, simply write down the content as is.
