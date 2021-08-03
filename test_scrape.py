import scrape

results_a = """
Event 4  Boys 2000 Meter Run CC 4th & Under
=======================================================================          
    Name                    Year School                  Finals  Points          
=======================================================================          
  1 #5537 Hynes, Eli           4 Tully Elementary       7:25.64    1             
  2 #2496 Lye, Sam             4 Harmony Elem           7:32.35    2             
  3  #363 Parke, Gannon        4 Beechwood El           7:35.83    3             
  4  #588 Perraut, Grant       4 Bourbon Central        7:37.51                  
  5  #365 Skeen, Charlie       4 Beechwood El           7:37.80    4             
  6 #2254 Terry, Jonah         3 Goshen Elementary      7:38.21    5             
  7 #2491 Killian, Oliver      4 Harmony Elem           7:38.60    6             
  8 #3712 Verbroekken, Kix     4 Middletown E           7:43.63                  
  9 #3653 Sierpina, Joseph     3 Meredith-Dun           7:44.00                  
 10 #5056 Reinhart, Mark       3 St. John School        7:44.46    7             
 11 #5799 Haskins, Andrew      3 Wilt Elementary        7:51.92    8             
 12 #1947 Watkins, Leo         3 Field Elementary       7:53.34    9             
 13 #3309 Chapman, Michael     3 Lincoln Elementary     7:57.47   10             
 14 #3414 Ellis, Mason         3 Lowe Element           7:57.90   11             
 15 #5105 Trauth, Cohen        4 St. Joseph,            7:59.02   12             
 16 #2700 Gordon, Rocco        4 Highlands La           7:59.87   13             
 17 #2257 Wells, Oliver        4 Goshen Elementary      8:00.35   14             
 18 #1069 Dillon, Jake         4 Centerfield            8:00.79   15             
 19 #3357 Klingenberg, Ty      4 Locust Grove           8:00.97   16             
 20 #3352 Felix, Owen          4 Locust Grove           8:01.26   17             
 21 #4364 Burgess, Andrew      4 Rosa Parks E           8:01.65   18             
 22 #2726 Robinson, William    3 Highlands La           8:02.22   19             
 23 #1603 Cameron, Will        4 Dunn Elementary        8:02.71   20             
 24 #4953 George, Eli          3 St. Agnes              8:03.60                  
 25 #2816 Smith, Trevor        4 Jesse D Lay            8:04.46                  
 26 #2173 White, Hayden        4 Glendover El           8:04.93   21             
 27 #1309 Eckler, Aaron        4 Longbranch             8:06.56   22             
 28  #359 Fohl, Abram          2 Beechwood El           8:07.40   23             
 29 #5290 Durst, Hayden        4 Stopher Elem           8:08.46   24             
 30  #803 Taylor, Hudson       4 Burgin                 8:09.30   25             
 31 #3310 Harter, Walker       4 Lincoln Elementary     8:11.25   26             
 32 #5108 Vandewater, Sam      4 St. Joseph,            8:12.90   27             
 33 #5308 Moore, Christopher   4 Stopher Elem           8:14.02   28             
 34 #5303 Lesshafft, Parker    4 Stopher Elem           8:15.33   29             
 35 #5773 Rosenbalm, Weston    4 Wilder Eleme           8:15.43   30             
 36 #5581 Jhaveri, Kamdyn      4 Villa Madonna          8:15.86   31             
 37 #5307 Mohr, Jack           4 Stopher Elem           8:16.01   32             
 38 #3429 Meacham, Malachi     3 Lowe Element           8:16.91   33             
 39 #4167 Wilson, Talon        4 Owen County            8:17.78                  
 40 #3359 Mulhall, Jackson     4 Locust Grove           8:18.15   34             
 41  #471 Crosby, Brooks       3 Bloom Elementary       8:18.43                  
 42 #5315 Wiseman, Amir        3 Stopher Elem           8:19.11   35             
 43 #1079 Springston, Graham   4 Centerfield            8:20.19   36             
 44 #2721 Nau, Judah           3 Highlands La           8:20.65   37             
 45  #687 Bertram, Kasen       3 Bracken County         8:22.71                  
 46 #5251 Glasgow, Salem       2 St. Thomas School      8:23.01   38             
 47 #1645 Stewart, Christian   4 Dunn Elementary        8:23.27   39             
 48 #4367 Fain, Colton         3 Rosa Parks E           8:23.89   40             
 49 #2495 Leksrisawat, Judah   3 Harmony Elem           8:24.61   41             
 50 #4752 Lemaster, Calliou    4 Second Stree           8:25.05   42             
 51 #4461 Bonzo, Sawyer        3 Russell                8:25.16   43             
 52 #3763 Boguszewski, Ben     4 Mount Washin           8:25.18                  
 53 #2289 Walters, Croix       4 Grant County           8:26.27                  
 54 #5117 Seymour, Cody        4 St. Margaret Mary      8:26.55                  
 55 #4697 Cash, Carter         4 Western Elementary     8:27.31                  
 56 #2719 Nau, Bennett         3 Highlands La           8:27.94   44             
 57  #805 Thompson, Hunter     4 Burgin                 8:28.51   45             
 58  #358 Fields, Mason        4 Beechwood El           8:28.65   46             
 59 #5258 West, Silas          2 St. Thomas School      8:28.67   47             
 60 #5535 Coyle, Porter        4 Tully Elementary       8:28.84   48             
 61 #5490 Calihan, Graham      4 Trinity Chri           8:29.19   49             
 62 #2485 Dunlap, Nate         4 Harmony Elem           8:29.36   50             
 63 #5804 Sudiswa, Adam        3 Wilt Elementary        8:30.44   51             
 64 #5771 Meyer, Shelby        4 Wilder Eleme           8:30.48   52             
 65  #362 Mooney, William      4 Beechwood El           8:30.83   53             
 66 #3041 York, Bryson         4 Lawrence County        8:30.88                  
 67 #1490 Dant, Tristyn        4 Eastview Elementary    8:31.22                  
 68 #1977 Vega, Jace           3 Flaherty Elementary    8:31.54   54             
 69 #5313 White, Alec          4 Stopher Elem           8:31.56   55             
 70 #5798 West, Owen           4 Williamstown           8:31.57                  
 71  #621 Newton, Landon       4 Bowen Elementary       8:32.17                  
 72 #2239 Marx, Connor         4 Goshen Elementary      8:32.30   56             
 73 #1939 O'Dell, Eli          2 Field Elementary       8:32.35   57             
 74 #3238 Dick, Jesse          3 Liberty Elem           8:32.91   58             
 75 #1031 Scott, Preston       4 Casey County           8:32.99                  
 76 #4759 Varble, Bronson      4 Second Stree           8:33.03   59             
 77 #5295 Flowers, Cash        3 Stopher Elem           8:33.39   60             
 78   #47 Mayes, Owen          4 Anchorage Pu           8:33.50                  
 79 #5299 Hearn, Truett        4 Stopher Elem           8:33.56                  
 80 #2488 Hong, JaeByn         2 Harmony Elem           8:33.63   61             
 81 #3431 Nazarkewich, Joshu   4 Lowe Element           8:33.65   62             
 82 #2498 Matthews, Kai        3 Harmony Elem           8:33.74   63             
 83 #5495 Heppner, Eric        4 Trinity Chri           8:35.36   64             
 84 #3605 Hall, Brayden        4 McBrayer Elementary    8:35.86   65             
 85 #2234 Johnson, Riley       4 Goshen Elementary      8:36.25   66             
 86 #2229 Hans, Ryland         4 Goshen Elementary      8:37.05   67             
 87 #3438 Sommer, Max          3 Lowe Element           8:37.34   68             
 88 #2786 Koetter, Hudson      4 Holy Spirit            8:39.00                  
 89 #1647 Weckman, Easton      4 Dunn Elementary        8:39.86   69             
 90  #404 Utley, Robert        4 Lebanon Junc           8:41.06                  
 91 #5500 Nichols, Garrett     3 Trinity Chri           8:42.77   70             
 92 #5125 Lea, Lucas           4 St. Mary               8:43.57   71             
 93  #221 Anselmo, Jase        4 Bates Elementary       8:43.72   72             
 94 #3347 Breeding, Ian        4 Locust Grove           8:44.22   73             
 95 #5168 Crawford, Miles      5 St. Matthews           8:44.95                  
 96 #2792 Gunderson, Beckett   4 Holy Trinity           8:45.15                  
 97 #1937 Metzger, Henry       3 Field Elementary       8:45.20   74             
 98 #1070 Doyle, Cooper        4 Centerfield            8:45.28   75             
 99 #5107 Vandewater, Joey     3 St. Joseph,            8:45.44   76             
100  #135 Kustelski, Trent     4 Athens-Chile           8:45.49                  
101 #4036 Hammond, Evan        4 Norton Elementary      8:45.56   77             
102 #5176 Milenthal, Atticus   4 St. Matthews           8:45.98                  
103 #5217 Rust, Garrett        3 St. Michael            8:46.62   78             
104 #5129 Shoulta, Tate        2 St. Mary               8:48.01   79             
105 #3376 Brown, Caleb         3 Louisville C           8:48.16                  
106 #5766 Lannon, Patrick      4 Wilder Eleme           8:48.86   80             
107 #2227 Gray, Jackson        3 Goshen Elementary      8:49.39   81             
109 #3252 Morgan, Jayden       4 Liberty Elem           8:50.09   83             
110 #1650 Woeste, James        4 Dunn Elementary        8:49.51   84             
110 #1650 Woeste, James        4 Dunn Elementary        8:50.41                  
111 #5570 Bowling, Garrett     3 University Heights     8:50.86                  
112 #1154 Brown, Fin           4 Cline Elemen           8:51.01                  
113 #3580 McClain, Preston     4 Maxwell Elem           8:51.24   85             
114 #2071 Lavey, Carson        3 Garden Sprin           8:51.35   86             
115 #3358 Mattera, Reid        3 Locust Grove           8:52.47   87             
116 #4365 Corbin, Scott        3 Rosa Parks E           8:53.14   88             
117 #5576 Fomby, Evan          4 Veteran's Pa           8:53.73                  
118 #1325 Ridings, Matthew     3 Longbranch             8:54.94   89             
119 #5767 Love, James          4 Wilder Eleme           8:55.10   90             
120 #1924 Bogel, Silas         4 Field Elementary       8:55.47   91             
121 #5045 Graham, Kieran       4 St. John School        8:55.53   92             
122 #4718 Russell, Eli         3 Stamping Ground        8:56.19                  
123 #2513 Wendling, Eli        4 Harmony Elem           8:56.33   93             
124 #4475 Qualls, Atreyu       3 Russell                8:57.11   94             
125 #2697 Falk, Leo            3 Highlands La           8:57.26   95             
126 #2480 Culver, Brody        4 Harmony Elem           8:57.49                  
127 #2522 Cooksey, Isaiah      4 Hawthorne El           8:58.21                  
128 #1308 Dunham, Henry        3 Longbranch             8:58.79   96             
129 #4263 Sobon, Leon          3 Providence C           8:59.65                  
130 #3920 Vasquez, Louis       4 North Hardin           9:00.07                  
131 #5104 Shewmaker, Brandon   3 St. Joseph,            9:00.50   97             
132 #1332 Stout, Brody         3 Longbranch             9:00.78   98             
133 #3241 Folsom, Caleb        3 Liberty Elem           9:01.73   99             
134 #4468 Floyd, Max           3 Russell                9:02.14  100             
135 #1965 Eikenberry, Noah     3 Flaherty Elementary    9:02.33  101             
136 #1963 Caster, Boss         4 Flaherty Elementary    9:02.88  102             
137 #5540 Ledford, Pete        4 Tully Elementary       9:03.50  103             
138 #5253 Middendorf, Max      3 St. Thomas School      9:03.58  104             
139 #5541 Mattingly, Preston   4 Tully Elementary       9:03.81  105             
140 #5208 Embry, Collin        3 St. Michael            9:04.20  106             
141 #2536 Porter, Gabe         4 Hawthorne El           9:04.46                  
142 #1510 Varble, Derek        3 Eastview Elementary    9:04.65                  
143 #3608 Jesse, Landon        4 McBrayer Elementary    9:04.95  107             
144 #2746 Brown, Gavin         4 Hite                   9:05.10  108             
145 #2062 Colthurst, Charlie   3 Garden Sprin           9:05.22  109             
146 #4576 Given, Mason         4 Sandy Hook E           9:05.28  110             
147 #4633 Miller, Luthur       4 Scapa Elementary       9:05.39                  
148 #3427 Luna, Damian         3 Lowe Element           9:05.82  111             
149 #4583 Holbrook, Payton     5 Sandy Hook E           9:06.17  112             
150  #236 Marler, Jaxon        4 Bates Elementary       9:07.35  113             
151 #2277 Kirk, Kenneth        4 Grant County           9:07.80                  
152 #5248 Darnell, Ian         4 St. Thomas School      9:08.06  114             
153  #360 Holliday, Matthew    4 Beechwood El           9:08.27  115             
154 #4043 Titus, Luke          3 Notre Dame A           9:08.50                  
155  #798 Mckenzie, Hayden     2 Burgin                 9:08.82  116             
156 #1979 Wellman, Cameron     4 Flaherty Elementary    9:09.25  117             
157 #1625 Haynes, Clark        2 Dunn Elementary        9:09.31  118             
158 #5542 Medley, Collin       4 Tully Elementary       9:09.73  119             
159 #4378 Naehr, Charlie       3 Rosa Parks E           9:09.92  120             
160  #222 Banks, Noah          2 Bates Elementary       9:10.13  121             
161  #364 Ritter, Colin        4 Beechwood El           9:10.17  122             
162 #3418 Gray, Alex           4 Lowe Element           9:10.74  123             
163 #3606 Holmes, Lincoln      1 McBrayer Elementary    9:10.94  124             
164 #5796 Osborne, William     4 Williamstown           9:11.01                  
165 #3764 Brown, Brady         2 Mount Washin           9:11.24                  
166 #5579 Degenhardt, Seth     4 Villa Madonna          9:12.48  125             
167 #1318 Janowiecki, Peyton   3 Longbranch             9:12.70  126             
168 #5106 Trauth, Gavin        3 St. Joseph,            9:12.86  127             
169 #4343 Bullen, Dalton       2 Rockcastle County      9:13.01                  
170   #50 Montgomery, Morgan   4 Anchorage Pu           9:13.24                  
171 #5401 Shively, Caden       4 The Lexingto           9:13.72                  
172 #4035 Conley, Scout        3 Norton Elementary      9:13.92  128             
173 #1073 Guerra-Rivera, Abe   4 Centerfield            9:14.18  129             
174 #2533 Pardo Sanchez, Joh   4 Hawthorne El           9:14.82                  
175 #5499 Mattern, Beck        4 Trinity Chri           9:15.28  130             
176 #5228 Alvey, Will          4 St. Patrick School     9:15.39                  
177 #5089 Clark, Matthew       4 St. Joseph,            9:15.96  131             
178 #5536 Hartlage, Caleb      3 Tully Elementary       9:16.02  132             
179 #5775 Woodson, Malcolm     3 Wilder Eleme           9:16.75  133             
180 #2424 Creech, Trey         2 Rosspoint El           9:18.02                  
181 #4242 Trimble, Patton      3 Pikeville              9:18.54                  
182 #4037 Hapuarachchi, Veth   3 Norton Elementary      9:19.22  134             
183 #1651 Woeste, William      1 Dunn Elementary        9:19.67  135             
184 #1933 Harvey, Arlo         2 Field Elementary       9:20.80  136             
185 #5256 Weinel, Gregory      3 St. Thomas School      9:21.37  137             
186  #234 Ludwick, Maxwell     4 Bates Elementary       9:21.71  138             
187 #4892 Hernandez, Diego     4 Southgate El           9:22.30                  
188 #3603 Armstrong, Duke      1 McBrayer Elementary    9:22.68  139             
189 #1930 Feaster, Jason       2 Field Elementary       9:22.82  140             
190  #248 Tichenor, Jacob      4 Bates Elementary       9:23.40  141             
191 #2765 Smith, Murphy        3 Hite                   9:23.64  142             
192 #1969 Hinton, Tony         4 Flaherty Elementary    9:23.94  143             
193 #4476 Roane, Landon        3 Russell                9:24.55  144             
194 #5126 Roark, Ethan         3 St. Mary               9:25.13  145             
195 #1962 Blake, Riley         4 Flaherty Elementary    9:25.15  146             
196 #1602 Brooker, Luke        3 Dunn Elementary        9:25.55                  
197 #1088 Mumford, Gabe        4 Chenoweth El           9:25.62                  
198 #2767 Tindall, Jack        4 Hite                   9:25.68  147             
199 #2728 Trocan, Gabriel      3 Highlands La           9:26.10  148             
200 #5188 Tremayne, Emery      3 St. Matthews           9:26.53                  
201 #4629 Edelen, Max          4 Scapa Elementary       9:26.89                  
202 #5398 Murry, Levi          4 The Lexingto           9:27.02                  
203 #5399 Pulito, Andrew       3 The Lexingto           9:27.32                  
204 #4466 Fain, Carson         2 Russell                9:27.50  149             
205 #5187 Simpson, Cruz        1 St. Matthews           9:27.99                  
206   #53 Normandin, Andre     4 Anchorage Pu           9:28.23                  
207 #2072 Navarro, Ikzander    4 Garden Sprin           9:28.48  150             
208 #5584 Webb, Zachary        4 Villa Madonna          9:28.61  151             
209 #4047 Fluhr, Kol           4 Old Mill Elementary    9:29.00                  
210  #623 Rietow, Breccan      2 Bowen Elementary       9:29.79                  
211 #1398 Smith, Levi          2 Crossroads E           9:30.02                  
212 #5252 Marx, Owen           3 St. Thomas School      9:32.11  152             
213 #5221 Stetar, Nathaniel    3 St. Michael            9:32.47  153             
214 #2529 Judah, Joe           4 Hawthorne El           9:32.71                  
215 #4372 Gupta, Ekansh        4 Rosa Parks E           9:33.42  154             
216 #4479 Sarver, Ian          4 Russell                9:33.52  155             
217 #2747 Carden, Jace         1 Hite                   9:33.69  156             
218 #5046 Graham, Owen         3 St. John School        9:33.83  157             
219 #2146 Chen, Jiaze          4 Glendover El           9:33.98  158             
220 #4246 Smith, Keagan        3 Pleasant Gro           9:35.92                  
221 #2084 Williams, Rhett      3 Garden Sprin           9:36.01  159             
222 #4374 Imamura, Masato      4 Rosa Parks E           9:36.18  160             
223 #4383 Rowe, Liam           4 Rosa Parks E           9:36.27  161             
224 #3420 Jackson, Charlie     3 Lowe Element           9:36.61  162             
225 #2233 Johnson, Landon      4 Goshen Elementary      9:37.27  163             
226 #1314 Hammons, Nolan       3 Longbranch             9:37.69  164             
227 #1833 Wainscott, Kota      3 Elkhorn Midd           9:37.87                  
228 #4034 Cease, Nathan        2 Norton Elementary      9:38.54  165             
229 #2058 Black, Lincoln       3 Garden Sprin           9:38.67  166             
230 #3316 Moldoveanu, Roman    4 Lincoln Elementary     9:39.82  167             
231 #5053 Mayer, Samual        2 St. John School        9:39.82  168             
232 #1449 Gaines, Bridger      3 Danville Chr           9:41.37                  
233 #1816 Alvis, Ryder         4 Elkhorn Elementary     9:41.92                  
234 #3650 Stine, Joshua        4 Mercer Elementary      9:42.09                  
235 #2076 Simmons, Jace        2 Garden Sprin           9:42.63  169             
236 #1959 Ballard, Urijah      4 Flaherty Elementary    9:42.81  170             
237 #2063 Dunne, Isaac         2 Garden Sprin           9:43.70  171             
238 #5770 Metzmeire, Luke      2 Wilder Eleme           9:43.80  172             
239 #1934 Hoyle, Johnathan     4 Field Elementary       9:44.26  173             
240 #4756 Schwaniger, Max      4 Second Stree           9:44.50  174             
241  #620 Newton, Austin       4 Bowen Elementary       9:44.86                  
242 #1800 Seow, Noah           2 Eisenhower E           9:45.28                  
243 #3244 Hudspeth, Tripp      2 Liberty Elem           9:45.43  175             
244  #695 Steinhauer, Mitche   4 Bracken County         9:45.46                  
245 #3313 Laughlin, Anson      3 Lincoln Elementary     9:46.00  176             
246 #3589 Vaughan, Judah       1 Maxwell Elem           9:47.69  177             
247 #5578 Degenhardt, Lucas    2 Villa Madonna          9:47.87  178             
248 #5214 Mcgill, Harley       3 St. Michael            9:48.19  179             
249 #2757 Minor, Gavin         2 Hite                   9:48.38  180             
250 #3579 Madison, Bryant      1 Maxwell Elem           9:48.41  181             
251 #4893 Hernandez, Xavi      3 Southgate El           9:48.41                  
252 #3762 Austin, Seth         3 Mount Washin           9:48.91                  
253 #5772 Nelson, Miles        4 Wilder Eleme           9:49.38  182             
254 #5321 Kreidenweis, Drew    4 Sts. Peter a           9:49.59                  
255 #2160 Moore, Jacob         3 Glendover El           9:50.38  183             
256 #5323 Kreidenweis, Riley   2 Sts. Peter a           9:51.41                  
257 #4568 Sallie, Ronan        2 Saints Peter           9:51.71                  
258 #4704 Johnson, Koen        4 Garth                  9:51.95                  
259 #4033 Calabrese, John      3 Norton Elementary      9:52.12  184             
260 #3578 Kern, Ryan           3 Maxwell Elem           9:53.52  185             
261 #4221 Wolfe, Levi          3 Pendleton County       9:55.27                  
262 #1801 Stone, Sam           3 Eisenhower E           9:55.69                  
263 #4478 Romero, Dominic      3 Russell                9:56.26  186             
264 #5583 Sebald, Isaac        3 Villa Madonna          9:56.82  187             
265  #253 Walls, Brayden       2 Bates Elementary       9:57.47  188             
266 #5122 Ashford, Trey        3 St. Mary               9:58.73  189             
267 #5802 Roller, Hunter       3 Wilt Elementary        9:59.30  190             
268 #5547 Whithem, Henley      3 Tully Elementary       9:59.83  191             
269 #1317 Iseral, Ashton       2 Longbranch            10:00.11  192             
270 #5504 Westerfield, Owen    3 Trinity Chri          10:00.63  193             
271 #4245 Farley, Finnegan     1 Pleasant Gro          10:01.45                  
272 #1496 Jones, Collin        4 Deerpark Elementary   10:02.63                  
273 #2166 Shaw, J G            3 Glendover El          10:02.89  194             
274 #2151 Hutchison, Archer    4 Glendover El          10:03.04  195             
275 #1022 Barnes, Ben          3 Casey County          10:03.59                  
276 #2764 Sanders, Ryan        3 Hite                  10:04.15  196             
277 #3321 Wilson, Sam          2 Lincoln Elementary    10:06.26  197             
278 #4159 Hearn, Ben           2 Owen County           10:06.93                  
279  #786 Berketis, Melvin     5 Burgin                10:07.33  198             
280 #3254 Roberts, Colton      1 Liberty Elem          10:07.38  199             
281 #5803 Rothgerber, Ashton   4 Wilt Elementary       10:08.28  200             
282 #1802 Valle, Jackson       4 Eisenhower E          10:09.03                  
283 #3315 Massey, Landon       2 Lincoln Elementary    10:09.77  201             
284 #5797 Shepherd, Elias      3 Williamstown          10:11.08                  
285 #3607 Jesse, Brady         2 McBrayer Elementary   10:11.26  202             
286 #5092 Dunlevy, Cameron     2 St. Joseph,           10:11.59  203             
287 #2142 Bahrani, Ayman       4 Glendover El          10:11.63  204             
288 #4748 Gaines, Landyn       3 Second Stree          10:12.85  205             
289 #1793 Forcht, Ryan         2 Eisenhower E          10:13.02                  
290 #2286 Schulcz, Kurt        4 Grant County          10:14.48                  
291 #2706 Hutcheson, Kaleb     2 Highlands La          10:16.28  206             
292 #4040 Rogers, Clayton      3 Norton Elementary     10:16.29  207             
293 #5123 Ault, Ben            1 St. Mary              10:16.59  208             
294  #527 Pieper, Christian    2 Collins Lane          10:17.58                  
295 #4050 Weddle, Colten       4 Old Mill Elementary   10:18.19                  
296 #3612 Shanklin, Brody      2 McBrayer Elementary   10:19.54  209             
297 #5893 Murray, Brady        2 Hite                  10:22.18  210             
298  #219 Andres, Ryker        2 Bates Elementary      10:22.68  211             
299 #4577 Guthrie, Cade        2 Sandy Hook E          10:23.42  212             
300 #3570 Duchesne, Henry      0 Maxwell Elem          10:23.63  213             
301 #5211 Howard, Keir         3 St. Michael           10:23.84  214             
302 #3576 Johnson, Cash        2 Maxwell Elem          10:26.18  215             
303 #5128 Shoulta, Cole        4 St. Mary              10:26.59  216             
304 #4575 Given, Jake          2 Sandy Hook E          10:27.06  217             
305 #4762 Wellman, Eli         1 Second Stree          10:27.08  218             
306  #520 Gudapati, Tanav      3 Collins Lane          10:28.09                  
307 #3604 Gross, Rylan         3 McBrayer Elementary   10:28.93  219             
308 #3233 Anderkin, Bryce      3 Liberty Elem          10:30.46  220             
309 #1077 Mowery, Hunter       4 Centerfield           10:31.08  221             
310 #5801 Neal, Caleb          4 Wilt Elementary       10:31.41  222             
311  #691 Leist, Kade          3 Bracken County        10:31.45                  
312 #5582 Kovacic, Avery       2 Villa Madonna         10:32.13  223             
313  #787 Berketis, Petros     4 Burgin                10:33.69  224             
314 #1072 Dykes, Baleon        2 Centerfield           10:36.34  225             
315  #806 Vandiviere, Zachar   0 Burgin                10:38.65  226             
316 #4230 Gibson, Caden Hawk   3 Phelps School         10:39.73  227             
317 #5320 Combs, Dylan         4 Sts. Peter a          10:42.46                  
318 #4760 Wainscott, Cal       4 Second Stree          10:42.83  228             
319 #4262 Miller, Daniel       3 Providence C          10:43.61                  
320  #690 Jefferson, Eli       3 Bracken County        10:44.49                  
321 #3253 Park, Asa            1 Liberty Elem          10:45.98  229             
322 #4233 Smith, Bucky         3 Phelps School         10:47.77  230             
323 #1028 Montgomery, Max      1 Casey County          10:48.78                  
324 #5124 Johnson, Benjamin    1 St. Mary              10:49.29  231             
325 #4229 Dotson, Drew         1 Phelps School         10:49.68  232             
326 #4706 Knight, Rhett        2 Stamping Ground       10:53.70                  
327 #4566 Hughson, Joshua      1 Saints Peter          10:54.68                  
328 #4747 Driskell, Robert     3 Second Stree          10:55.16  233             
329  #518 Gautam, Madhu        3 Bridgeport            10:55.83                  
330 #5048 Hughes, Griffin      3 St. John School       10:56.23  234             
331 #1820 Bratton, Kolston     3 Peaks Mill            10:56.83                  
332 #3828 Collins, Peyton      3 Mullins School        10:57.64                  
333 #4717 Richardson, Wyatt    3 Stamping Ground       10:57.78                  
334 #5322 Kreidenweis, Luke    2 Sts. Peter a          10:58.26                  
335 #2143 Baro Reyes, Octavi   4 Glendover El          10:59.15  235             
336 #1080 Vazquez, Nicolas     3 Centerfield           10:59.91  236             
337 #2385 Stevens, Gideon      4 Greenup Elementary    11:10.45                  
338  #673 Thacker, Grant       2 Boyd County           11:10.65                  
339 #2430 Sanders, Carson      2 Rosspoint El          11:12.61                  
340   #24 Alexander, Holt      2 Anchorage Pu          11:15.29                  
341 #5800 Miller, Eli          1 Wilt Elementary       11:18.78  237             
342 #1399 Stickling, Ethan     3 Crossroads E          11:18.82                  
343 #5232 Gondim, Nicholas     3 St. Patrick School    11:24.63                  
344 #3829 Harvey, Benjamin     4 Mullins School        11:28.43                  
345 #5502 Schornick, Sutton    2 Trinity Chri          11:29.78  238             
346 #3577 Johnson-Breazeale,   1 Maxwell Elem          11:31.72  239             
347  #625 Shekhovtsov, Andre   1 Bowen Elementary      11:33.58                  
348  #672 Lucas, Sean          2 Boyd County           11:37.32                  
349 #5227 Albritton, Asher     2 St. Patrick School    11:46.62                  
350 #4702 Garmon, Grayer       3 Anne Mason            11:48.19                  
351  #528 Risk, Hiatt          1 Bridgeport            11:54.10                  
352  #794 Cochran, Judson      0 Burgin                11:55.87  240             
353 #4891 Duty, Cameron        2 Southgate El          12:04.84                  
354 #4038 McCoy, Jackson       2 Norton Elementary     12:05.85  241             
355  #402 Rogers, Bentley      1 Lebanon Junc          12:07.76                  
356 #4231 Gooslin, Kevin       2 Phelps School         12:11.12  242             
357 #1830 Seward, Dade         3 Hearn                 12:11.41                  
358 #3830 Isaac, Caleb         4 Mullins School        12:15.94                  
359 #4232 Hurley, Brettley     2 Phelps School         12:17.01  243             
360 #2386 Wireman, Flynn       2 Greenup Elementary    12:18.62                  
361 #5059 Walters, Samual      4 St. John School       12:43.26  244             
362 #4636 Vaish, Shiva         4 Scapa Elementary      12:46.94                  
363 #2423 Collins, Zakk        0 Rosspoint El          12:50.95                  
364 #2384 Brown, Isaac         2 Greenup Elementary    12:51.99                  
365 #1447 Carney, Owen         2 Danville Chr          12:53.55                  
366 #4698 Deaton, Danny        1 Garth                 12:57.01                  
367 #4582 Holbrook, Brody      1 Sandy Hook E          13:07.12  245             
368 #1027 Gaines, Kenneth      2 Casey County          13:24.90                  
369  #517 Cirillo, Johnathon   3 Collins Lane          13:26.25                  
370 #1450 Gaines, Judah        1 Danville Chr          13:26.89                  
371 #3318 Stearman, Linus      4 Lincoln Elementary    13:29.89  246             
372 #4630 Hummel, Tyler        4 Scapa Elementary      13:33.49                  
373  #403 Simon, Jameson       3 Cedar Grove           13:50.42                  
374 #4228 Compton Jr, David    2 Phelps School         14:26.00  247             
                                                                                 
                                   Team Scores                                   
=================================================================================
Rank Team                      Total    1    2    3    4    5   *6   *7   *8   *9
=================================================================================
   1 Beechwood Elementary        129    3    4   23   46   53  115  122          
      Total Time:    40:20.51                                                    
         Average:     8:04.11                                                    
   2 Stopher Elementary School   148   24   28   29   32   35   55   60          
      Total Time:    41:12.93                                                    
         Average:     8:14.59                                                    
   3 Harmony Elementary School   160    2    6   41   50   61   63   93          
      Total Time:    40:38.55                                                    
         Average:     8:07.71                                                    
   4 Goshen Elementary           208    5   14   56   66   67   81  163          
      Total Time:    41:24.16                                                    
         Average:     8:16.84                                                    
   5 Highlands Latin School El   208   13   19   37   44   95  148  206          
      Total Time:    41:47.94                                                    
         Average:     8:21.59                                                    
   6 Locust Grove Elementary S   227   16   17   34   73   87                    
      Total Time:    41:57.07                                                    
         Average:     8:23.42                                                    
   7 Lowe Elementary School      285   11   33   62   68  111  123  162          
      Total Time:    42:31.62                                                    
         Average:     8:30.33                                                    
   8 Dunn Elementary             330   20   39   69   84  118  135               
      Total Time:    43:04.66                                                    
         Average:     8:36.94                                                    
   9 St. Joseph, Cold Spring     339   12   27   76   97  127  131  203          
      Total Time:    43:10.72                                                    
         Average:     8:38.15                                                    
  10 Field Elementary            367    9   57   74   91  136  140  173          
      Total Time:    43:27.16                                                    
         Average:     8:41.44                                                    
  11 Tully Elementary            376    1   48  103  105  119  132  191          
      Total Time:    43:11.52                                                    
         Average:     8:38.31                                                    
  12 Wilder Elementary School    385   30   52   80   90  133  172  182          
      Total Time:    43:46.62                                                    
         Average:     8:45.33                                                    
  13 Rosa Parks Elementary       420   18   40   88  120  154  160  161          
      Total Time:    44:02.02                                                    
         Average:     8:48.41                                                    
  14 Longbranch                  431   22   89   96   98  126  164  192          
      Total Time:    44:13.77                                                    
         Average:     8:50.76                                                    
  15 St. Thomas School           440   38   47  104  114  137  152               
      Total Time:    44:24.69                                                    
         Average:     8:52.94                                                    
  16 Centerfield Elementary Sc   476   15   36   75  129  221  225  236          
      Total Time:    44:51.52                                                    
         Average:     8:58.31                                                    
  17 Trinity Christian Academy   506   49   64   70  130  193  238               
      Total Time:    45:03.23                                                    
         Average:     9:00.65                                                    
  18 Flaherty Elementary         517   54  101  102  117  143  146  170          
      Total Time:    45:09.94                                                    
         Average:     9:01.99                                                    
  19 Russell                     530   43   94  100  144  149  155  186          
      Total Time:    45:16.46                                                    
         Average:     9:03.30                                                    
  20 Lincoln Elementary          576   10   26  167  176  197  201  246          
      Total Time:    45:40.80                                                    
         Average:     9:08.16                                                    
  21 Bates Elementary            585   72  113  121  138  141  188  211          
      Total Time:    45:46.31                                                    
         Average:     9:09.27                                                    
  22 Burgin                      608   25   45  116  198  224  226  240          
      Total Time:    46:27.65                                                    
         Average:     9:17.53                                                    
  23 Liberty Elementary School   614   58   83   99  175  199  220  229          
      Total Time:    46:17.54                                                    
         Average:     9:15.51                                                    
  24 McBrayer Elementary         637   65  107  124  139  202  209  219          
      Total Time:    46:25.69                                                    
         Average:     9:17.14                                                    
  25 St. John School             658    7   92  157  168  234  244               
      Total Time:    46:49.87                                                    
         Average:     9:21.98                                                    
  26 Garden Springs Elementary   670   86  109  150  159  166  169  171          
      Total Time:    46:39.73                                                    
         Average:     9:19.95                                                    
  27 Wilt Elementary             671    8   51  190  200  222  237               
      Total Time:    47:01.35                                                    
         Average:     9:24.27                                                    
  28 Villa Madonna               672   31  125  151  178  187  223               
      Total Time:    46:41.64                                                    
         Average:     9:20.33                                                    
  29 Norton Elementary           688   77  128  134  165  184  207  241          
      Total Time:    46:49.36                                                    
         Average:     9:21.88                                                    
  30 St. Mary                    692   71   79  145  189  208  216  231          
      Total Time:    47:12.03                                                    
         Average:     9:26.41                                                    
  31 Second Street Elementary    698   42   59  174  205  218  228  233          
      Total Time:    47:22.51                                                    
         Average:     9:28.51                                                    
  32 St. Michael                 730   78  106  153  179  214                    
      Total Time:    47:35.32                                                    
         Average:     9:31.07                                                    
  33 Hite                        733  108  142  147  156  180  196  210          
      Total Time:    47:16.49                                                    
         Average:     9:27.30                                                    
  34 Glendover Elementary        751   21  158  183  194  195  204  235          
      Total Time:    47:35.22                                                    
         Average:     9:31.05                                                    
  35 Maxwell Elementary School   841   85  177  181  185  213  215  239          
      Total Time:    48:44.49                                                    
         Average:     9:44.90                                                    
  36 Sandy Hook Elementary       896  110  112  212  217  245                    
      Total Time:    52:09.05                                                    
         Average:    10:25.81                                                    
  37 Phelps School              1174  227  230  232  242  243  247               
      Total Time:    56:45.31                                                    
         Average:    11:21.07 """

def test_get_runners():
    runners = scrape.get_runners(results_a)
    # should be a list
    assert isinstance(runners, list)
    assert len(runners) == 374


def test_scrape():
    url = "https://ky.milesplit.com/meets/364782-ktccca-meet-of-champions-2019/results/676374/raw"
    results = scrape.get_raw_results(url)
    assert results != None
    assert "Name" in results
    assert "Event" in results
    assert results == results_a
    runners = scrape.get_runners(results)
    assert len(runners) == 374
    scrape.write_csv("364782-ktccca-meet-of-champions-2019.csv", runners)

def test_2019_tiger_run():
    url = "https://ky.milesplit.com/meets/341354-tiger-run-2019/results/660303/raw"
    results = scrape.get_raw_results(url)
    assert results != None
    assert "Name" in results
    assert "Event" in results
    runners = scrape.get_runners(results)
    assert len(runners) == 332

    scrape.write_csv("341354-tiger-run-2019.csv", runners)

def test_reader():
    runners = scrape.read_csv("341354-tiger-run-2019.csv")
    assert len(runners) == 332+1