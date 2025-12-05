//-----------------------------------------------------------------------------
//  TIVA_Param.h
// 
//-----------------------------------------------------------------------------

#define PORT_LED_R     PF_1
#define PORT_LED_G     PF_2
#define PORT_LED_B     PF_3
#define PORT_POTAR     PE_3
#define PORT_BOUTON    PC_6
#define PORT_LM35TEMP  PD_1
#define PORT_ADA1063   PD_0


//------------------------------------------------------------------------------------
// Fonctions de l Afficheur OLED
//------------------------------------------------------------------------------------
void    AOLED_InitScreen(void);
void    AOLED_InvertDisplay(short invert);
void    AOLED_AffiLogoIsep(void);
void    AOLED_ClearScreen(void);
void    AOLED_ClearLine(short numlin);
void    AOLED_FillScreen(char value);
void    AOLED_FillLine(short numlin, char value);
void    AOLED_WriteColonne(char value, short nbcol);
void    AOLED_DisplayImage(const char* pBuff);
void    AOLED_DisplayCarac(short numcol, short numlin, char car);
void    AOLED_DisplayTexte(short numcol, short numlin, char* texte);
