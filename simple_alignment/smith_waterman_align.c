#include <ctype.h>
#include <unistd.h>
#include <getopt.h>

#include "utilities.h"
#include "sequences.h"

// should I print the debug stuff?
bool debug_flag = FALSE;

#define SUB 0
#define INS 1
#define DEL 2

// show the alignment?
bool show_alignment = FALSE;

void smith_waterman_align(const char* const file1, const char* const file2)
{
    // read the sequences from the fasta file
    sequence* s1= read_fasta_sequence(file1);
    uchar* t1   = (uchar*)copy_string((char*)s1->sequence);
    close_fasta_sequence(s1);
    if(TRUE == debug_flag) printf("%s\n", t1);

    sequence* s2= read_fasta_sequence(file2);
    uchar* t2   = (uchar*)copy_string((char*)s2->sequence);
    close_fasta_sequence(s2);
    if(TRUE == debug_flag) printf("%s\n", t2);

    uint len1 = strlen((char*)t1);
    uint len2 = strlen((char*)t2);

    // counters in loops
    uint i, j;

    // initialize the scores
    int match    = 2;
    int mismatch = 1;
    int gopen    = 4;
    int gextend  = 1;

    // allocate the dp matrix
    int** V = ckalloc((len2 + 1)*sizeof(int*));
    for(i = 0; i <= len2; i++){
        V[i] = ckallocz((len1 + 1) * sizeof(int));
        V[i][0] = -gopen -(i*gextend);
    }
    for(j = 0; j <= len1; j++){
        V[0][j] = -gopen -(j*gextend);
    }

    // allocate E,F (two other variables to fill the dp matrix)
    int E;
    int* F = ckallocz((len1+1)*sizeof(int));

    // keep track of the indices for backtracking
    char** I = ckalloc((len2 + 1)*sizeof(char*));
    for(i = 0; i <= len2; i++){
        I[i] = ckallocz((len1 + 1) * sizeof(char));
    }

    // variables to store intermediate values if this is a sub/indel.
    int ifsub, ifdel, ifins, ifindel;

    // maximum score of the alignment
    int max_score = 0, max_i = -1, max_j = -1;

    // find the scores for the dp matrix
    for(i = 1; i <= len2; i++){
        E = 0;
        for(j = 1; j <= len1; j++){
            ifsub = V[i-1][j-1];
            ifsub = toupper(t1[j-1]) == toupper(t2[i-1]) ? \
                                        ifsub + match : ifsub - mismatch;

            ifins = MAX(F[j], V[i-1][j] - gopen) - gextend;
            F[j]  = ifins;
            
            ifdel = MAX(E, V[i][j-1] - gopen) - gextend;
            E     = ifdel;

            ifindel = MAX(ifins, ifdel);

            // priority if the scores are equal are subs, ins, del.
            V[i][j] = ifsub;
            I[i][j] = SUB;
            if(V[i][j] < ifindel){
                if(ifins >= ifdel) I[i][j] = INS; else I[i][j] = DEL;
                V[i][j] = ifindel;
            }

            // an alignment which includes more bases from the reference is
            // given preference, hence the >=
            if(V[i][j] >= max_score){
                max_score = V[i][j];
                max_i     = i;
                max_j     = j;
            }
        }
    }
    ckfree(F);
   
    // lets print out the dp matrix to check
    if(TRUE == debug_flag){ 
        printf("----------DP MATRIX--------\n");
        for(i = 0; i <= len2; i++){
            for(j = 0; j <= len1; j++){
                printf("%d\t", V[i][j]);
            }
            printf("\n");
        }
    }
     if(TRUE == debug_flag){ 
        printf("----------INDEX MATRIX--------\n");
        for(i = 0; i <= len2; i++){
            for(j = 0; j <= len1; j++){
                printf("%d\t", I[i][j]);
            }
            printf("\n");
        }
    }
   
    char* nt1 = ckallocz((len1+len2)*sizeof(char));
    char* nt2 = ckallocz((len1+len2)*sizeof(char));

    // trace back to find the best alignment
    char direction = SUB;
    int flag  = -1, score = max_score;
    uint a = 0, b = 0;
    i = max_i;
    j = max_j;
    while(score > 0){
        direction = I[i][j];
        I[i][j]   = flag;
        if(SUB == direction){
            nt1[a++] = t1[j-1];
            nt2[b++] = t2[i-1];
            i--; j--;
        }else if(INS == direction){
            nt1[a++] = '-';
            nt2[b++] = t2[i-1];
            i--;
        }else{
            nt1[a++] = t1[j-1];
            nt2[b++] = '-';
            j--;
        }
        flag  = direction;
        score = V[i][j];
    }

    ckfree(t1);
    ckfree(t2);

    assert(strlen(nt1) == strlen(nt2));
    
    int k, subs = 0, ins = 0, dels = 0;
    for(k = strlen(nt1); k >= 0; k--){
        if(nt1[k] == '-'){
            ins++;
        }else if(nt2[k] == '-'){
            dels++;
        }else if(nt1[k] != nt2[k]){
            subs++;
        }
    }   
    
    if(show_alignment == FALSE){
        printf("%d substitutions, %d insertions, %d deletions\n", 
                subs, ins, dels);
    }

    if(show_alignment == TRUE){
        printf("#text1 text2\n");
        for(k = strlen(nt1); k >= 0; k--) printf("%c", nt1[k]);     
        printf(" ");
        for(k = strlen(nt2); k >= 0; k--) printf("%c", nt2[k]);     
        printf("\n");
    }

    // free all these resources
    ckfree(nt1);
    ckfree(nt2);

    for(i = 0; i <= len2; i++){
        ckfree(V[i]);
    }
    ckfree(V);
    for(i = 0; i <= len2; i++){
        ckfree(I[i]);
    }
    ckfree(I);
    
    return;
}

extern char* optarg;
extern int optopt;

int main(int argc, char** argv)
{
    int c;
    
    char* file1 = NULL;
    char* file2 = NULL;

    while((c = getopt(argc, argv, "a:b:ds")) != -1){
        switch(c){
            case 'a': file1 = optarg;        break;
            case 'b': file2 = optarg;        break;
            case 'd': debug_flag = TRUE;     break;
            case 's': show_alignment = TRUE; break;
            case '?': 
                if (optopt == 'a'){
                    fprintf(stderr,"Option 'a' requires an argument.");
                }else if(isprint(optopt)){
                    fprintf (stderr, "Unknown option `-%c'.\n", optopt);
                }else{
                    fprintf (stderr,\
                    "Unknown option character `\\x%x'.\n", optopt);
                }
                return EXIT_FAILURE;
            default : abort();
        }
    }

    if(file1 == NULL || file2 == NULL){
        fatalf("Please specify 2 files as input -a ref.fa -b tar.fa");
    }

    smith_waterman_align(file1, file2);

    return EXIT_SUCCESS;
}
